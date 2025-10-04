import logging
import ccxt
from decimal import Decimal
from celery import shared_task
from django.utils import timezone
from django.core.cache import cache
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task
def update_market_data():
    """Update market data for all trading pairs"""
    try:
        from .models import TradingPair, MarketData
        
        # Get all active trading pairs
        trading_pairs = TradingPair.objects.filter(is_active=True)
        
        for pair in trading_pairs:
            try:
                # Update market data for this pair
                update_pair_market_data.delay(pair.id)
                
            except Exception as e:
                logger.error(f"Error updating market data for pair {pair.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in update_market_data: {str(e)}")
        raise

@shared_task
def update_price_feeds():
    """Update price feeds from exchanges"""
    try:
        from .models import Exchange, TradingPair, Ticker
        
        # Get all active exchanges
        exchanges = Exchange.objects.filter(is_active=True)
        
        for exchange in exchanges:
            try:
                # Update price feeds for this exchange
                update_exchange_price_feeds.delay(exchange.id)
                
            except Exception as e:
                logger.error(f"Error updating price feeds for exchange {exchange.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in update_price_feeds: {str(e)}")
        raise

@shared_task
def update_pair_market_data(pair_id):
    """Update market data for a specific trading pair"""
    try:
        from .models import TradingPair, MarketData, Ticker
        
        pair = TradingPair.objects.get(id=pair_id)
        
        # Get latest ticker data
        ticker = Ticker.objects.filter(
            trading_pair=pair.symbol
        ).order_by('-timestamp').first()
        
        if not ticker:
            logger.warning(f"No ticker data found for pair {pair.symbol}")
            return False
        
        # Create or update market data
        market_data, created = MarketData.objects.get_or_create(
            trading_pair=pair.symbol,
            timestamp=timezone.now().replace(second=0, microsecond=0),  # Round to minute
            defaults={
                'open_price': ticker.last_price,
                'high_price': ticker.high_price,
                'low_price': ticker.low_price,
                'close_price': ticker.last_price,
                'volume': ticker.volume,
                'quote_volume': ticker.quote_volume,
            }
        )
        
        if not created:
            # Update existing market data
            market_data.high_price = max(market_data.high_price, ticker.high_price)
            market_data.low_price = min(market_data.low_price, ticker.low_price)
            market_data.close_price = ticker.last_price
            market_data.volume = ticker.volume
            market_data.quote_volume = ticker.quote_volume
            market_data.save()
        
        logger.info(f"Updated market data for {pair.symbol}")
        return True
        
    except TradingPair.DoesNotExist:
        logger.error(f"Trading pair {pair_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error updating market data for pair {pair_id}: {str(e)}")
        raise

@shared_task
def update_exchange_price_feeds(exchange_id):
    """Update price feeds for a specific exchange"""
    try:
        from .models import Exchange, TradingPair, Ticker
        
        exchange = Exchange.objects.get(id=exchange_id)
        
        # Get trading pairs for this exchange
        trading_pairs = TradingPair.objects.filter(
            exchange=exchange,
            is_active=True
        )
        
        for pair in trading_pairs:
            try:
                # Update ticker for this pair
                update_ticker.delay(exchange.id, pair.symbol)
                
            except Exception as e:
                logger.error(f"Error updating ticker for {pair.symbol}: {str(e)}")
                continue
        
        return True
        
    except Exchange.DoesNotExist:
        logger.error(f"Exchange {exchange_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error updating price feeds for exchange {exchange_id}: {str(e)}")
        raise

@shared_task
def update_ticker(exchange_id, trading_pair):
    """Update ticker data for a specific exchange and trading pair"""
    try:
        from .models import Exchange, Ticker
        
        exchange = Exchange.objects.get(id=exchange_id)
        
        # Simulate fetching ticker data from exchange
        # In a real implementation, this would use the exchange's API
        import random
        
        # Generate mock ticker data
        base_price = Decimal('50000')  # Base price for BTC
        price_change = random.uniform(-0.05, 0.05)  # ±5% change
        current_price = base_price * (1 + price_change)
        
        high_price = current_price * (1 + random.uniform(0, 0.02))
        low_price = current_price * (1 - random.uniform(0, 0.02))
        volume = Decimal(str(random.uniform(100, 1000)))
        quote_volume = volume * current_price
        
        # Create ticker record
        ticker = Ticker.objects.create(
            exchange=exchange.name,
            trading_pair=trading_pair,
            last_price=current_price,
            high_price=high_price,
            low_price=low_price,
            volume=volume,
            quote_volume=quote_volume,
            timestamp=timezone.now(),
        )
        
        logger.info(f"Updated ticker for {trading_pair} on {exchange.name}: ${current_price:.2f}")
        return True
        
    except Exchange.DoesNotExist:
        logger.error(f"Exchange {exchange_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error updating ticker for {trading_pair}: {str(e)}")
        raise

@shared_task
def update_order_book(exchange_id, trading_pair):
    """Update order book for a specific exchange and trading pair"""
    try:
        from .models import Exchange, OrderBook
        
        exchange = Exchange.objects.get(id=exchange_id)
        
        # Simulate fetching order book data
        # In a real implementation, this would use the exchange's API
        import random
        
        # Generate mock order book data
        base_price = Decimal('50000')
        
        # Generate bids (buy orders)
        bids = []
        for i in range(10):
            price = base_price * (1 - (i * 0.001))  # Decreasing prices
            quantity = Decimal(str(random.uniform(0.1, 2.0)))
            bids.append([float(price), float(quantity)])
        
        # Generate asks (sell orders)
        asks = []
        for i in range(10):
            price = base_price * (1 + (i * 0.001))  # Increasing prices
            quantity = Decimal(str(random.uniform(0.1, 2.0)))
            asks.append([float(price), float(quantity)])
        
        # Create order book record
        order_book = OrderBook.objects.create(
            exchange=exchange.name,
            trading_pair=trading_pair,
            bids=bids,
            asks=asks,
            timestamp=timezone.now(),
        )
        
        logger.info(f"Updated order book for {trading_pair} on {exchange.name}")
        return True
        
    except Exchange.DoesNotExist:
        logger.error(f"Exchange {exchange_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error updating order book for {trading_pair}: {str(e)}")
        raise

@shared_task
def update_trade_history(exchange_id, trading_pair):
    """Update trade history for a specific exchange and trading pair"""
    try:
        from .models import Exchange, Trade
        
        exchange = Exchange.objects.get(id=exchange_id)
        
        # Simulate fetching trade history
        # In a real implementation, this would use the exchange's API
        import random
        
        # Generate mock trade data
        base_price = Decimal('50000')
        
        for _ in range(5):  # Create 5 mock trades
            price = base_price * (1 + random.uniform(-0.02, 0.02))
            quantity = Decimal(str(random.uniform(0.01, 1.0)))
            side = random.choice(['buy', 'sell'])
            
            trade = Trade.objects.create(
                exchange=exchange.name,
                trading_pair=trading_pair,
                trade_id=f"mock_trade_{timezone.now().timestamp()}_{random.randint(1000, 9999)}",
                price=price,
                quantity=quantity,
                side=side,
                timestamp=timezone.now(),
            )
        
        logger.info(f"Updated trade history for {trading_pair} on {exchange.name}")
        return True
        
    except Exchange.DoesNotExist:
        logger.error(f"Exchange {exchange_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error updating trade history for {trading_pair}: {str(e)}")
        raise

@shared_task
def aggregate_market_data():
    """Aggregate market data across exchanges"""
    try:
        from .models import TradingPair, AggregatedMarketData
        
        # Get all trading pairs
        trading_pairs = TradingPair.objects.filter(is_active=True)
        
        for pair in trading_pairs:
            try:
                # Aggregate data for this pair
                aggregate_pair_data.delay(pair.symbol)
                
            except Exception as e:
                logger.error(f"Error aggregating data for {pair.symbol}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in aggregate_market_data: {str(e)}")
        raise

@shared_task
def aggregate_pair_data(trading_pair):
    """Aggregate market data for a specific trading pair"""
    try:
        from .models import Ticker, AggregatedMarketData
        
        # Get all tickers for this pair from the last hour
        tickers = Ticker.objects.filter(
            trading_pair=trading_pair,
            timestamp__gte=timezone.now() - timezone.timedelta(hours=1)
        )
        
        if not tickers.exists():
            logger.warning(f"No ticker data found for {trading_pair}")
            return False
        
        # Calculate aggregated values
        prices = [t.last_price for t in tickers]
        volumes = [t.volume for t in tickers]
        
        avg_price = sum(prices) / len(prices)
        total_volume = sum(volumes)
        min_price = min(prices)
        max_price = max(prices)
        
        # Create aggregated record
        aggregated_data = AggregatedMarketData.objects.create(
            trading_pair=trading_pair,
            timestamp=timezone.now().replace(minute=0, second=0, microsecond=0),  # Round to hour
            average_price=avg_price,
            high_price=max_price,
            low_price=min_price,
            total_volume=total_volume,
            trade_count=tickers.count(),
        )
        
        logger.info(f"Aggregated market data for {trading_pair}")
        return True
        
    except Exception as e:
        logger.error(f"Error aggregating data for {trading_pair}: {str(e)}")
        raise

@shared_task
def cleanup_old_market_data():
    """Clean up old market data records"""
    try:
        from .models import Ticker, MarketData, OrderBook, Trade, AggregatedMarketData
        
        # Keep data for different periods
        cutoff_ticker = timezone.now() - timezone.timedelta(days=7)
        cutoff_market_data = timezone.now() - timezone.timedelta(days=30)
        cutoff_order_book = timezone.now() - timezone.timedelta(days=1)
        cutoff_trade = timezone.now() - timezone.timedelta(days=7)
        cutoff_aggregated = timezone.now() - timezone.timedelta(days=90)
        
        # Delete old records
        deleted_tickers = Ticker.objects.filter(timestamp__lt=cutoff_ticker).delete()
        deleted_market_data = MarketData.objects.filter(timestamp__lt=cutoff_market_data).delete()
        deleted_order_books = OrderBook.objects.filter(timestamp__lt=cutoff_order_book).delete()
        deleted_trades = Trade.objects.filter(timestamp__lt=cutoff_trade).delete()
        deleted_aggregated = AggregatedMarketData.objects.filter(timestamp__lt=cutoff_aggregated).delete()
        
        logger.info(f"Cleaned up old market data: {deleted_tickers[0]} tickers, {deleted_market_data[0]} market data, {deleted_order_books[0]} order books, {deleted_trades[0]} trades, {deleted_aggregated[0]} aggregated data")
        
        return True
        
    except Exception as e:
        logger.error(f"Error cleaning up old market data: {str(e)}")
        raise 