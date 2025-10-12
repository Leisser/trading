"""
Celery tasks for trade execution and updates
"""
from celery import shared_task
from decimal import Decimal
from django.utils import timezone
from django.db import transaction as db_transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_active_trades():
    """
    Update all active trades by decreasing trade_sum and calculating P&L.
    Runs every 5 seconds via Celery beat.
    """
    from .models import Trade
    from wallets.models import MultiCurrencyWallet, CryptoBalance
    
    # Get all active strategy trades with trade_sum > 0
    active_trades = Trade.objects.filter(
        is_strategy_trade=True,
        status='pending',
        trade_sum__gt=0
    ).select_related('cryptocurrency', 'user')
    
    channel_layer = get_channel_layer()
    updated_count = 0
    
    for trade in active_trades:
        try:
            with db_transaction.atomic():
                # Simulate price movement (random walk)
                import random
                price_change = (random.random() - 0.5) * 0.02  # ±1% change
                current_price = float(trade.price) * (1 + price_change)
                
                # Calculate P&L
                entry_price = float(trade.entry_price) if trade.entry_price else float(trade.price)
                price_diff = current_price - entry_price
                pnl_percentage = (price_diff / entry_price) * 100
                pnl = float(trade.amount) * price_diff * trade.leverage
                
                # Decrease trade_sum by 2% per interval
                current_trade_sum = float(trade.trade_sum)
                trading_rate = 0.02  # 2% per interval
                traded_amount = current_trade_sum * trading_rate
                new_trade_sum = max(0, current_trade_sum - traded_amount)
                
                # Update trade
                trade.trade_sum = Decimal(str(new_trade_sum))
                trade.price = Decimal(str(current_price))
                trade.pnl = Decimal(str(pnl))
                
                # Check if completed
                if new_trade_sum <= 0:
                    trade.status = 'executed'
                    trade.executed_at = timezone.now()
                    
                    # Send completion notification via WebSocket
                    async_to_sync(channel_layer.group_send)(
                        f'trades_user_{trade.user.id}',
                        {
                            'type': 'trade_completed',
                            'trade_id': trade.id,
                            'final_pnl': str(pnl),
                            'timestamp': timezone.now().isoformat()
                        }
                    )
                else:
                    # Send update via WebSocket
                    async_to_sync(channel_layer.group_send)(
                        f'trades_user_{trade.user.id}',
                        {
                            'type': 'trade_update',
                            'trade_id': trade.id,
                            'trade_sum': str(new_trade_sum),
                            'current_price': str(current_price),
                            'pnl': str(pnl),
                            'status': trade.status,
                            'timestamp': timezone.now().isoformat()
                        }
                    )
                
                trade.save()
                updated_count += 1
                
        except Exception as e:
            logger.error(f"Error updating trade {trade.id}: {str(e)}")
            continue
    
    logger.info(f"Updated {updated_count} active trades")
    return updated_count


@shared_task
def stop_trade_and_return_balance(trade_id):
    """
    Stop a trade and return the remaining trade_sum to user's balance.
    Called when user manually stops a trade.
    """
    from .models import Trade
    from wallets.models import MultiCurrencyWallet, CryptoBalance
    
    try:
        trade = Trade.objects.get(id=trade_id)
        
        if trade.trade_sum <= 0:
            return {'success': False, 'error': 'Trade already completed'}
        
        with db_transaction.atomic():
            # Calculate amount to return (proportional to remaining trade_sum)
            initial_deduction = float(trade.total_value)
            remaining_percentage = float(trade.trade_sum) / float(trade.amount) if float(trade.amount) > 0 else 0
            amount_to_return = Decimal(str(initial_deduction * remaining_percentage))
            
            # Get user wallet
            wallet = MultiCurrencyWallet.objects.get(user=trade.user)
            
            # Get USDT balance
            from .models import Cryptocurrency
            usdt = Cryptocurrency.objects.get(symbol='USDT')
            usdt_balance, _ = CryptoBalance.objects.get_or_create(
                wallet=wallet,
                cryptocurrency=usdt,
                defaults={'balance': Decimal('0')}
            )
            
            # Return balance
            usdt_balance.balance += amount_to_return
            usdt_balance.save()
            
            # Update trade status
            trade.status = 'cancelled'
            trade.save()
            
            # Send balance update via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'trades_user_{trade.user.id}',
                {
                    'type': 'balance_update',
                    'balance': str(usdt_balance.balance),
                    'currency': 'USDT',
                    'reason': 'trade_stopped',
                    'amount_returned': str(amount_to_return),
                    'timestamp': timezone.now().isoformat()
                }
            )
            
            return {
                'success': True,
                'amount_returned': str(amount_to_return),
                'new_balance': str(usdt_balance.balance)
            }
            
    except Exception as e:
        logger.error(f"Error stopping trade {trade_id}: {str(e)}")
        return {'success': False, 'error': str(e)}
