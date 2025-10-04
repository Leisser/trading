"""
Advanced Trading Services for sophisticated order management and execution.
"""
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from typing import Dict, List, Optional
import logging

from .advanced_models import AdvancedOrder, TradingStrategy, OrderExecution, StrategyExecution
from risk_management.services import RiskManagementService
from compliance.services import ComplianceService

logger = logging.getLogger(__name__)

class AdvancedTradingService:
    """Service for advanced trading operations"""
    
    @staticmethod
    def create_stop_loss_order(user, symbol: str, side: str, quantity: Decimal, 
                              stop_price: Decimal, **kwargs) -> AdvancedOrder:
        """Create a stop-loss order"""
        # Risk management checks
        risk_service = RiskManagementService()
        if not risk_service.check_position_size(quantity):
            raise ValueError("Position size exceeds risk limits")
        
        # Compliance checks
        compliance_service = ComplianceService()
        if compliance_service.is_kyc_required(quantity * stop_price) and not user.kyc_verified:
            raise ValueError("KYC verification required for this trade amount")
        
        order = AdvancedOrder.objects.create(
            user=user,
            order_type='stop_loss',
            symbol=symbol,
            side=side,
            quantity=quantity,
            stop_price=stop_price,
            **kwargs
        )
        
        logger.info(f"Created stop-loss order {order.id} for {user.email}")
        return order
    
    @staticmethod
    def create_take_profit_order(user, symbol: str, side: str, quantity: Decimal,
                                limit_price: Decimal, **kwargs) -> AdvancedOrder:
        """Create a take-profit order"""
        # Risk management checks
        risk_service = RiskManagementService()
        if not risk_service.check_position_size(quantity):
            raise ValueError("Position size exceeds risk limits")
        
        order = AdvancedOrder.objects.create(
            user=user,
            order_type='take_profit',
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=limit_price,
            **kwargs
        )
        
        logger.info(f"Created take-profit order {order.id} for {user.email}")
        return order
    
    @staticmethod
    def create_limit_order(user, symbol: str, side: str, quantity: Decimal,
                          price: Decimal, **kwargs) -> AdvancedOrder:
        """Create a limit order"""
        # Risk management checks
        risk_service = RiskManagementService()
        if not risk_service.check_position_size(quantity):
            raise ValueError("Position size exceeds risk limits")
        
        order = AdvancedOrder.objects.create(
            user=user,
            order_type='limit',
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            **kwargs
        )
        
        logger.info(f"Created limit order {order.id} for {user.email}")
        return order
    
    @staticmethod
    def create_market_order(user, symbol: str, side: str, quantity: Decimal, **kwargs) -> AdvancedOrder:
        """Create a market order"""
        # Risk management checks
        risk_service = RiskManagementService()
        if not risk_service.check_position_size(quantity):
            raise ValueError("Position size exceeds risk limits")
        
        order = AdvancedOrder.objects.create(
            user=user,
            order_type='market',
            symbol=symbol,
            side=side,
            quantity=quantity,
            **kwargs
        )
        
        # Market orders are executed immediately
        AdvancedTradingService.execute_market_order(order)
        
        logger.info(f"Created and executed market order {order.id} for {user.email}")
        return order
    
    @staticmethod
    def create_stop_limit_order(user, symbol: str, side: str, quantity: Decimal,
                               stop_price: Decimal, limit_price: Decimal, **kwargs) -> AdvancedOrder:
        """Create a stop-limit order"""
        # Risk management checks
        risk_service = RiskManagementService()
        if not risk_service.check_position_size(quantity):
            raise ValueError("Position size exceeds risk limits")
        
        order = AdvancedOrder.objects.create(
            user=user,
            order_type='stop_limit',
            symbol=symbol,
            side=side,
            quantity=quantity,
            stop_price=stop_price,
            limit_price=limit_price,
            **kwargs
        )
        
        logger.info(f"Created stop-limit order {order.id} for {user.email}")
        return order
    
    @staticmethod
    def execute_market_order(order: AdvancedOrder) -> bool:
        """Execute a market order immediately"""
        try:
            with transaction.atomic():
                # Get current market price (simulated)
                current_price = AdvancedTradingService.get_current_price(order.symbol)
                
                # Create execution record
                execution = OrderExecution.objects.create(
                    order=order,
                    execution_time=timezone.now(),
                    executed_quantity=order.quantity,
                    execution_price=current_price,
                    fees=order.quantity * current_price * Decimal('0.001')  # 0.1% fee
                )
                
                # Update order status
                order.status = 'filled'
                order.filled_quantity = order.quantity
                order.average_fill_price = current_price
                order.total_fees = execution.fees
                order.filled_at = timezone.now()
                order.save()
                
                logger.info(f"Executed market order {order.id} at {current_price}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to execute market order {order.id}: {str(e)}")
            order.status = 'rejected'
            order.save()
            return False
    
    @staticmethod
    def get_current_price(symbol: str) -> Decimal:
        """Get current market price for a symbol (simulated)"""
        # In a real implementation, this would fetch from an exchange API
        # For now, return a simulated price
        price_map = {
            'BTC/USDT': Decimal('45000.00'),
            'ETH/USDT': Decimal('3000.00'),
            'BNB/USDT': Decimal('300.00'),
        }
        return price_map.get(symbol, Decimal('100.00'))
    
    @staticmethod
    def execute_strategy(strategy: TradingStrategy) -> Dict:
        """Execute a trading strategy"""
        try:
            with transaction.atomic():
                # Get strategy parameters
                params = strategy.parameters
                
                # Execute based on strategy type
                if strategy.strategy_type == 'dca':
                    result = AdvancedTradingService.execute_dca_strategy(strategy, params)
                elif strategy.strategy_type == 'grid':
                    result = AdvancedTradingService.execute_grid_strategy(strategy, params)
                elif strategy.strategy_type == 'momentum':
                    result = AdvancedTradingService.execute_momentum_strategy(strategy, params)
                else:
                    result = {'action': 'hold', 'reason': 'Strategy type not implemented'}
                
                # Record strategy execution
                StrategyExecution.objects.create(
                    strategy=strategy,
                    execution_time=timezone.now(),
                    action=result.get('action', 'hold'),
                    symbol=strategy.symbol,
                    quantity=result.get('quantity'),
                    price=result.get('price'),
                    reason=result.get('reason', ''),
                    pnl=result.get('pnl')
                )
                
                # Update strategy
                strategy.last_executed = timezone.now()
                strategy.save()
                
                logger.info(f"Executed strategy {strategy.id} for {strategy.user.email}")
                return result
                
        except Exception as e:
            logger.error(f"Failed to execute strategy {strategy.id}: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def execute_dca_strategy(strategy: TradingStrategy, params: Dict) -> Dict:
        """Execute Dollar Cost Averaging strategy"""
        # DCA logic would go here
        return {
            'action': 'buy',
            'quantity': params.get('amount', Decimal('100')),
            'reason': 'DCA buy signal triggered'
        }
    
    @staticmethod
    def execute_grid_strategy(strategy: TradingStrategy, params: Dict) -> Dict:
        """Execute Grid Trading strategy"""
        # Grid trading logic would go here
        return {
            'action': 'hold',
            'reason': 'Grid levels not reached'
        }
    
    @staticmethod
    def execute_momentum_strategy(strategy: TradingStrategy, params: Dict) -> Dict:
        """Execute Momentum Trading strategy"""
        # Momentum trading logic would go here
        return {
            'action': 'hold',
            'reason': 'Momentum indicators neutral'
        }

class OrderManagementService:
    """Service for order management operations"""
    
    @staticmethod
    def cancel_order(order: AdvancedOrder) -> bool:
        """Cancel a pending order"""
        try:
            if order.status != 'pending':
                return False
            
            order.status = 'cancelled'
            order.cancelled_at = timezone.now()
            order.save()
            
            logger.info(f"Cancelled order {order.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cancel order {order.id}: {str(e)}")
            return False
    
    @staticmethod
    def modify_order(order: AdvancedOrder, **updates) -> bool:
        """Modify an existing order"""
        try:
            if order.status != 'pending':
                return False
            
            # Update order fields
            for field, value in updates.items():
                if hasattr(order, field):
                    setattr(order, field, value)
            
            order.save()
            
            logger.info(f"Modified order {order.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to modify order {order.id}: {str(e)}")
            return False
    
    @staticmethod
    def get_order_summary(user) -> Dict:
        """Get order summary for a user"""
        orders = AdvancedOrder.objects.filter(user=user)
        
        return {
            'total_orders': orders.count(),
            'pending_orders': orders.filter(status='pending').count(),
            'filled_orders': orders.filter(status='filled').count(),
            'cancelled_orders': orders.filter(status='cancelled').count(),
            'total_volume': sum(order.quantity for order in orders.filter(status='filled')),
            'total_fees': sum(order.total_fees for order in orders.filter(status='filled'))
        }
    
    @staticmethod
    def check_stop_orders(symbol: str, current_price: Decimal) -> List[AdvancedOrder]:
        """Check and trigger stop orders"""
        triggered_orders = []
        
        # Get pending stop orders for the symbol
        stop_orders = AdvancedOrder.objects.filter(
            symbol=symbol,
            status='pending',
            order_type__in=['stop_loss', 'stop_limit']
        )
        
        for order in stop_orders:
            if order.order_type == 'stop_loss':
                # Check if stop price is reached
                if order.side == 'buy' and current_price >= order.stop_price:
                    triggered_orders.append(order)
                elif order.side == 'sell' and current_price <= order.stop_price:
                    triggered_orders.append(order)
            
            elif order.order_type == 'stop_limit':
                # Check if stop price is reached and convert to limit order
                if order.side == 'buy' and current_price >= order.stop_price:
                    order.order_type = 'limit'
                    order.price = order.limit_price
                    order.stop_price = None
                    order.save()
                    triggered_orders.append(order)
                elif order.side == 'sell' and current_price <= order.stop_price:
                    order.order_type = 'limit'
                    order.price = order.limit_price
                    order.stop_price = None
                    order.save()
                    triggered_orders.append(order)
        
        return triggered_orders
