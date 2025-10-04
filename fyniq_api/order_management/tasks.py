import logging
from decimal import Decimal
from celery import shared_task
from django.utils import timezone
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task
def process_pending_orders():
    """Process pending orders"""
    try:
        from .models import Order
        
        # Get pending orders - fixed to match actual model fields
        pending_orders = Order.objects.filter(
            status='pending',
            created_at__gte=timezone.now() - timezone.timedelta(hours=1)  # Only recent orders
        ).select_related('user')
        
        for order in pending_orders:
            try:
                with transaction.atomic():
                    # Check if order should be executed
                    if should_execute_order(order):
                        execute_order.delay(order.id)
                    elif should_cancel_order(order):
                        cancel_order.delay(order.id)
                        
            except Exception as e:
                logger.error(f"Error processing order {order.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in process_pending_orders: {str(e)}")
        raise

@shared_task
def execute_order(order_id):
    """Execute a specific order"""
    try:
        from .models import Order, OrderFill
        from market_data.models import Ticker
        from portfolio_management.models import Position, Balance
        
        order = Order.objects.select_related('user').get(id=order_id)
        
        if order.status != 'pending':
            logger.warning(f"Order {order_id} is not pending, status: {order.status}")
            return False
        
        # Get current market price - simplified since we don't have trading_pair relationship
        # For now, we'll use a placeholder price
        current_price = Decimal('50000')  # Placeholder price
        
        # Check if order can be filled at current price
        if order.order_type == 'market':
            # Market orders are filled immediately
            fill_price = current_price
        elif order.order_type == 'limit':
            if order.side == 'buy' and current_price <= order.price:
                fill_price = order.price
            elif order.side == 'sell' and current_price >= order.price:
                fill_price = order.price
            else:
                # Order cannot be filled at current price
                return False
        else:
            logger.error(f"Unsupported order type: {order.order_type}")
            return False
        
        with transaction.atomic():
            # Create order fill
            fill = OrderFill.objects.create(
                order=order,
                fill_id=f"fill_{order_id}_{timezone.now().timestamp()}",
                quantity=order.quantity,
                price=fill_price,
                quote_amount=order.quantity * fill_price,
                filled_at=timezone.now(),
            )
            
            # Update order status
            order.status = 'filled'
            order.filled_quantity = order.quantity
            order.average_fill_price = fill_price
            order.total_quote_amount = order.quantity * fill_price
            order.filled_at = timezone.now()
            order.save()
            
            # Update user balance - simplified
            update_user_balance(order.user, order, fill_price)
            
            # Update or create position - simplified
            update_user_position(order.user, order, fill_price)
            
            # Trigger portfolio update
            from portfolio_management.tasks import update_portfolio_values
            update_portfolio_values.delay(order.user.id)
            
            logger.info(f"Order {order_id} executed at {fill_price}")
            
        return True
        
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error executing order {order_id}: {str(e)}")
        raise

@shared_task
def cancel_order(order_id):
    """Cancel a specific order"""
    try:
        from .models import Order
        
        order = Order.objects.get(id=order_id)
        
        if order.status not in ['pending', 'partially_filled']:
            logger.warning(f"Order {order_id} cannot be cancelled, status: {order.status}")
            return False
        
        with transaction.atomic():
            order.status = 'cancelled'
            order.cancelled_at = timezone.now()
            order.save()
            
            logger.info(f"Order {order_id} cancelled")
            
        return True
        
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error cancelling order {order_id}: {str(e)}")
        raise

@shared_task
def process_algorithmic_orders():
    """Process algorithmic orders"""
    try:
        from .models import OrderAlgo
        
        # Get active algorithmic orders
        algo_orders = OrderAlgo.objects.filter(
            is_active=True,
            created_at__gte=timezone.now() - timezone.timedelta(days=7)  # Only recent orders
        ).select_related('order', 'order__user')
        
        for algo_order in algo_orders:
            try:
                # Check if conditions are met
                if check_algo_conditions(algo_order):
                    # Create regular order
                    create_order_from_algo.delay(algo_order.id)
                    
            except Exception as e:
                logger.error(f"Error processing algo order {algo_order.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in process_algorithmic_orders: {str(e)}")
        raise

@shared_task
def create_order_from_algo(algo_order_id):
    """Create a regular order from algorithmic order"""
    try:
        from .models import OrderAlgo, Order
        
        algo_order = OrderAlgo.objects.get(id=algo_order_id)
        
        # Create regular order
        order = Order.objects.create(
            user=algo_order.order.user,
            order_id=f"algo_{algo_order_id}_{timezone.now().timestamp()}",
            trading_pair=algo_order.order.trading_pair,
            base_currency=algo_order.order.base_currency,
            quote_currency=algo_order.order.quote_currency,
            order_type=algo_order.order.order_type,
            side=algo_order.order.side,
            quantity=algo_order.order.quantity,
            price=algo_order.order.price,
            status='pending',
        )
        
        logger.info(f"Created order {order.id} from algo order {algo_order_id}")
        
        return order.id
        
    except OrderAlgo.DoesNotExist:
        logger.error(f"Algorithmic order {algo_order_id} not found")
        return None
    except Exception as e:
        logger.error(f"Error creating order from algo {algo_order_id}: {str(e)}")
        raise

def should_execute_order(order):
    """Check if order should be executed"""
    # Add your order execution logic here
    # This could include market conditions, risk checks, etc.
    return True

def should_cancel_order(order):
    """Check if order should be cancelled"""
    # Add your order cancellation logic here
    # This could include time-based cancellation, market conditions, etc.
    return False

def calculate_fee(order, price):
    """Calculate trading fee"""
    # Add your fee calculation logic here
    # This could be based on exchange, volume, user tier, etc.
    fee_rate = Decimal('0.001')  # 0.1% fee
    return order.quantity * price * fee_rate

def update_user_balance(user, order, price):
    """Update user balance after order execution"""
    from portfolio_management.models import Balance
    
    total_value = order.quantity * price
    
    if order.side == 'buy':
        # Deduct quote currency, add base currency
        quote_balance, _ = Balance.objects.get_or_create(
            user=user,
            currency=order.quote_currency,
            defaults={'amount': Decimal('0')}
        )
        quote_balance.amount -= total_value
        quote_balance.save()
        
        base_balance, _ = Balance.objects.get_or_create(
            user=user,
            currency=order.base_currency,
            defaults={'amount': Decimal('0')}
        )
        base_balance.amount += order.quantity
        base_balance.save()
        
    else:  # sell
        # Deduct base currency, add quote currency
        base_balance, _ = Balance.objects.get_or_create(
            user=user,
            currency=order.base_currency,
            defaults={'amount': Decimal('0')}
        )
        base_balance.amount -= order.quantity
        base_balance.save()
        
        quote_balance, _ = Balance.objects.get_or_create(
            user=user,
            currency=order.quote_currency,
            defaults={'amount': Decimal('0')}
        )
        quote_balance.amount += total_value
        quote_balance.save()

def update_user_position(user, order, price):
    """Update user position after order execution"""
    from portfolio_management.models import Position
    
    # Create a simple position tracking
    position, created = Position.objects.get_or_create(
        user=user,
        trading_pair=order.trading_pair,
        defaults={
            'amount': Decimal('0'),
            'avg_entry_price': Decimal('0'),
        }
    )
    
    if order.side == 'buy':
        # Add to position
        total_amount = position.amount + order.quantity
        total_value = (position.amount * position.avg_entry_price) + (order.quantity * price)
        position.amount = total_amount
        position.avg_entry_price = total_value / total_amount if total_amount > 0 else Decimal('0')
    else:
        # Reduce position
        position.amount -= order.quantity
        if position.amount <= 0:
            position.delete()
            return
    
    position.save()

def check_algo_conditions(algo_order):
    """Check if algorithmic order conditions are met"""
    # Add your algorithmic order condition checking logic here
    # This could include technical indicators, price levels, etc.
    return False 