import logging
from decimal import Decimal
from celery import shared_task
from django.utils import timezone
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task
def execute_trading_strategy(strategy_id):
    """Execute a trading strategy"""
    try:
        from .models import TradingStrategy
        
        strategy = TradingStrategy.objects.get(id=strategy_id)
        
        if not strategy.is_active:
            logger.info(f"Strategy {strategy_id} is not active")
            return False
        
        # Execute strategy logic
        if strategy.strategy_type == 'moving_average':
            execute_moving_average_strategy.delay(strategy_id)
        elif strategy.strategy_type == 'rsi':
            execute_rsi_strategy.delay(strategy_id)
        elif strategy.strategy_type == 'bollinger_bands':
            execute_bollinger_bands_strategy.delay(strategy_id)
        else:
            logger.error(f"Unknown strategy type: {strategy.strategy_type}")
            return False
        
        return True
        
    except TradingStrategy.DoesNotExist:
        logger.error(f"Trading strategy {strategy_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error executing trading strategy {strategy_id}: {str(e)}")
        raise

@shared_task
def execute_moving_average_strategy(strategy_id):
    """Execute moving average crossover strategy"""
    try:
        from .models import TradingStrategy
        from market_data.models import Ticker
        from order_management.models import Order
        
        strategy = TradingStrategy.objects.get(id=strategy_id)
        
        # Get recent price data
        tickers = Ticker.objects.filter(
            trading_pair=strategy.trading_pair
        ).order_by('-timestamp')[:50]  # Last 50 ticks
        
        if tickers.count() < 50:
            logger.warning(f"Insufficient data for strategy {strategy_id}")
            return False
        
        # Calculate moving averages
        prices = [t.last_price for t in tickers]
        short_ma = sum(prices[:20]) / 20  # 20-period MA
        long_ma = sum(prices) / 50  # 50-period MA
        
        # Check for crossover signals
        if short_ma > long_ma and strategy.last_signal != 'buy':
            # Golden cross - buy signal
            order = Order.objects.create(
                user=strategy.user,
                trading_pair=strategy.trading_pair,
                order_type='market',
                side='buy',
                amount=strategy.position_size,
                status='pending',
                strategy=strategy,
            )
            
            strategy.last_signal = 'buy'
            strategy.last_executed = timezone.now()
            strategy.save()
            
            logger.info(f"Buy signal executed for strategy {strategy_id}")
            
        elif short_ma < long_ma and strategy.last_signal != 'sell':
            # Death cross - sell signal
            # Check if user has position to sell
            from portfolio_management.models import Position
            
            position = Position.objects.filter(
                user=strategy.user,
                trading_pair=strategy.trading_pair
            ).first()
            
            if position and position.amount > 0:
                order = Order.objects.create(
                    user=strategy.user,
                    trading_pair=strategy.trading_pair,
                    order_type='market',
                    side='sell',
                    amount=position.amount,
                    status='pending',
                    strategy=strategy,
                )
                
                strategy.last_signal = 'sell'
                strategy.last_executed = timezone.now()
                strategy.save()
                
                logger.info(f"Sell signal executed for strategy {strategy_id}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error executing moving average strategy {strategy_id}: {str(e)}")
        raise

@shared_task
def execute_rsi_strategy(strategy_id):
    """Execute RSI strategy"""
    try:
        from .models import TradingStrategy
        from market_data.models import Ticker
        from order_management.models import Order
        
        strategy = TradingStrategy.objects.get(id=strategy_id)
        
        # Get recent price data
        tickers = Ticker.objects.filter(
            trading_pair=strategy.trading_pair
        ).order_by('-timestamp')[:14]  # Last 14 ticks for RSI
        
        if tickers.count() < 14:
            logger.warning(f"Insufficient data for RSI strategy {strategy_id}")
            return False
        
        # Calculate RSI
        prices = [t.last_price for t in tickers]
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i-1] - prices[i]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / len(gains)
        avg_loss = sum(losses) / len(losses)
        
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        
        # Check for RSI signals
        if rsi < 30 and strategy.last_signal != 'buy':  # Oversold
            order = Order.objects.create(
                user=strategy.user,
                trading_pair=strategy.trading_pair,
                order_type='market',
                side='buy',
                amount=strategy.position_size,
                status='pending',
                strategy=strategy,
            )
            
            strategy.last_signal = 'buy'
            strategy.last_executed = timezone.now()
            strategy.save()
            
            logger.info(f"RSI buy signal executed for strategy {strategy_id} (RSI: {rsi:.2f})")
            
        elif rsi > 70 and strategy.last_signal != 'sell':  # Overbought
            from portfolio_management.models import Position
            
            position = Position.objects.filter(
                user=strategy.user,
                trading_pair=strategy.trading_pair
            ).first()
            
            if position and position.amount > 0:
                order = Order.objects.create(
                    user=strategy.user,
                    trading_pair=strategy.trading_pair,
                    order_type='market',
                    side='sell',
                    amount=position.amount,
                    status='pending',
                    strategy=strategy,
                )
                
                strategy.last_signal = 'sell'
                strategy.last_executed = timezone.now()
                strategy.save()
                
                logger.info(f"RSI sell signal executed for strategy {strategy_id} (RSI: {rsi:.2f})")
        
        return True
        
    except Exception as e:
        logger.error(f"Error executing RSI strategy {strategy_id}: {str(e)}")
        raise

@shared_task
def execute_bollinger_bands_strategy(strategy_id):
    """Execute Bollinger Bands strategy"""
    try:
        from .models import TradingStrategy
        from market_data.models import Ticker
        from order_management.models import Order
        
        strategy = TradingStrategy.objects.get(id=strategy_id)
        
        # Get recent price data
        tickers = Ticker.objects.filter(
            trading_pair=strategy.trading_pair
        ).order_by('-timestamp')[:20]  # Last 20 ticks
        
        if tickers.count() < 20:
            logger.warning(f"Insufficient data for Bollinger Bands strategy {strategy_id}")
            return False
        
        # Calculate Bollinger Bands
        prices = [t.last_price for t in tickers]
        sma = sum(prices) / len(prices)
        
        # Calculate standard deviation
        variance = sum((p - sma) ** 2 for p in prices) / len(prices)
        std_dev = variance ** 0.5
        
        upper_band = sma + (2 * std_dev)
        lower_band = sma - (2 * std_dev)
        current_price = prices[0]
        
        # Check for Bollinger Bands signals
        if current_price <= lower_band and strategy.last_signal != 'buy':  # Price at lower band
            order = Order.objects.create(
                user=strategy.user,
                trading_pair=strategy.trading_pair,
                order_type='market',
                side='buy',
                amount=strategy.position_size,
                status='pending',
                strategy=strategy,
            )
            
            strategy.last_signal = 'buy'
            strategy.last_executed = timezone.now()
            strategy.save()
            
            logger.info(f"Bollinger Bands buy signal executed for strategy {strategy_id}")
            
        elif current_price >= upper_band and strategy.last_signal != 'sell':  # Price at upper band
            from portfolio_management.models import Position
            
            position = Position.objects.filter(
                user=strategy.user,
                trading_pair=strategy.trading_pair
            ).first()
            
            if position and position.amount > 0:
                order = Order.objects.create(
                    user=strategy.user,
                    trading_pair=strategy.trading_pair,
                    order_type='market',
                    side='sell',
                    amount=position.amount,
                    status='pending',
                    strategy=strategy,
                )
                
                strategy.last_signal = 'sell'
                strategy.last_executed = timezone.now()
                strategy.save()
                
                logger.info(f"Bollinger Bands sell signal executed for strategy {strategy_id}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error executing Bollinger Bands strategy {strategy_id}: {str(e)}")
        raise

@shared_task
def backtest_strategy(strategy_id, start_date, end_date):
    """Backtest a trading strategy"""
    try:
        from .models import TradingStrategy, BacktestResult
        from market_data.models import Ticker
        
        strategy = TradingStrategy.objects.get(id=strategy_id)
        
        # Get historical data
        tickers = Ticker.objects.filter(
            trading_pair=strategy.trading_pair,
            timestamp__range=[start_date, end_date]
        ).order_by('timestamp')
        
        if not tickers.exists():
            logger.error(f"No historical data found for backtest")
            return False
        
        # Initialize backtest variables
        initial_balance = 10000  # $10,000 starting balance
        current_balance = initial_balance
        position = 0
        trades = []
        
        # Run backtest
        for ticker in tickers:
            # Apply strategy logic (simplified)
            # This would use the same logic as the live strategies
            pass
        
        # Calculate results
        final_balance = current_balance
        total_return = final_balance - initial_balance
        return_percentage = (total_return / initial_balance) * 100
        
        # Save backtest results
        BacktestResult.objects.create(
            strategy=strategy,
            start_date=start_date,
            end_date=end_date,
            initial_balance=initial_balance,
            final_balance=final_balance,
            total_return=total_return,
            return_percentage=return_percentage,
            total_trades=len(trades),
            win_rate=0,  # Calculate based on trades
            max_drawdown=0,  # Calculate based on balance history
        )
        
        logger.info(f"Backtest completed for strategy {strategy_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error backtesting strategy {strategy_id}: {str(e)}")
        raise

@shared_task
def optimize_strategy_parameters(strategy_id):
    """Optimize strategy parameters using machine learning"""
    try:
        from .models import TradingStrategy
        
        strategy = TradingStrategy.objects.get(id=strategy_id)
        
        # This would implement parameter optimization
        # For now, just log the task
        logger.info(f"Parameter optimization requested for strategy {strategy_id}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error optimizing strategy {strategy_id}: {str(e)}")
        raise

@shared_task
def monitor_strategy_performance():
    """Monitor performance of all active strategies"""
    try:
        from .models import TradingStrategy
        
        active_strategies = TradingStrategy.objects.filter(is_active=True)
        
        for strategy in active_strategies:
            try:
                # Calculate strategy performance metrics
                calculate_strategy_performance.delay(strategy.id)
                
            except Exception as e:
                logger.error(f"Error monitoring strategy {strategy.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in monitor_strategy_performance: {str(e)}")
        raise

@shared_task
def calculate_strategy_performance(strategy_id):
    """Calculate performance metrics for a strategy"""
    try:
        from .models import TradingStrategy, StrategyPerformance
        
        strategy = TradingStrategy.objects.get(id=strategy_id)
        
        # Get recent trades for this strategy
        from order_management.models import Order
        
        recent_orders = Order.objects.filter(
            strategy=strategy,
            created_at__gte=timezone.now() - timezone.timedelta(days=30)
        )
        
        # Calculate metrics
        total_trades = recent_orders.count()
        winning_trades = recent_orders.filter(realized_pnl__gt=0).count()
        losing_trades = recent_orders.filter(realized_pnl__lt=0).count()
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = sum(order.realized_pnl for order in recent_orders if order.realized_pnl)
        avg_win = sum(order.realized_pnl for order in recent_orders if order.realized_pnl and order.realized_pnl > 0) / winning_trades if winning_trades > 0 else 0
        avg_loss = sum(order.realized_pnl for order in recent_orders if order.realized_pnl and order.realized_pnl < 0) / losing_trades if losing_trades > 0 else 0
        
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else 0
        
        # Create or update performance record
        performance, created = StrategyPerformance.objects.get_or_create(
            strategy=strategy,
            period='30d',
            defaults={
                'start_date': timezone.now().date() - timezone.timedelta(days=30),
                'end_date': timezone.now().date(),
            }
        )
        
        performance.total_trades = total_trades
        performance.winning_trades = winning_trades
        performance.losing_trades = losing_trades
        performance.win_rate = win_rate
        performance.total_pnl = total_pnl
        performance.avg_win = avg_win
        performance.avg_loss = avg_loss
        performance.profit_factor = profit_factor
        performance.save()
        
        logger.info(f"Performance calculated for strategy {strategy_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error calculating strategy performance {strategy_id}: {str(e)}")
        raise 