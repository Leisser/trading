"""
Market Data Services for real-time cryptocurrency data integration.
"""
import ccxt
import pandas as pd
from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from .models import Exchange, TradingPair, MarketData, PriceAlert
import logging
import asyncio
import aiohttp
from typing import Dict, List, Optional
import json

logger = logging.getLogger(__name__)

class MarketDataService:
    """Service for fetching and managing real-time market data"""
    
    def __init__(self):
        self.exchanges = {
            'binance': ccxt.binance({
                'apiKey': getattr(settings, 'BINANCE_API_KEY', ''),
                'secret': getattr(settings, 'BINANCE_SECRET', ''),
                'sandbox': getattr(settings, 'BINANCE_SANDBOX', True),
            }),
            'coinbase': ccxt.coinbasepro({
                'apiKey': getattr(settings, 'COINBASE_API_KEY', ''),
                'secret': getattr(settings, 'COINBASE_SECRET', ''),
                'passphrase': getattr(settings, 'COINBASE_PASSPHRASE', ''),
            }),
            'kraken': ccxt.kraken({
                'apiKey': getattr(settings, 'KRAKEN_API_KEY', ''),
                'secret': getattr(settings, 'KRAKEN_SECRET', ''),
            })
        }
    
    def get_real_time_price(self, symbol: str, exchange: str = 'binance') -> Dict:
        """Get real-time price for a symbol from specified exchange"""
        try:
            exchange_instance = self.exchanges.get(exchange)
            if not exchange_instance:
                raise ValueError(f"Exchange {exchange} not supported")
            
            ticker = exchange_instance.fetch_ticker(symbol)
            
            return {
                'symbol': symbol,
                'exchange': exchange,
                'price': Decimal(str(ticker['last'])),
                'bid': Decimal(str(ticker['bid'])),
                'ask': Decimal(str(ticker['ask'])),
                'volume': Decimal(str(ticker['baseVolume'])),
                'change_24h': Decimal(str(ticker['change'])),
                'change_percent_24h': Decimal(str(ticker['percentage'])),
                'high_24h': Decimal(str(ticker['high'])),
                'low_24h': Decimal(str(ticker['low'])),
                'timestamp': timezone.now()
            }
        except Exception as e:
            logger.error(f"Error fetching price for {symbol} from {exchange}: {str(e)}")
            return None
    
    def get_ohlcv_data(self, symbol: str, timeframe: str = '1h', limit: int = 100, exchange: str = 'binance') -> List[Dict]:
        """Get OHLCV data for a symbol"""
        try:
            exchange_instance = self.exchanges.get(exchange)
            if not exchange_instance:
                raise ValueError(f"Exchange {exchange} not supported")
            
            ohlcv = exchange_instance.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            data = []
            for candle in ohlcv:
                data.append({
                    'timestamp': timezone.datetime.fromtimestamp(candle[0] / 1000),
                    'open': Decimal(str(candle[1])),
                    'high': Decimal(str(candle[2])),
                    'low': Decimal(str(candle[3])),
                    'close': Decimal(str(candle[4])),
                    'volume': Decimal(str(candle[5]))
                })
            
            return data
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {symbol}: {str(e)}")
            return []
    
    def get_order_book(self, symbol: str, exchange: str = 'binance', limit: int = 20) -> Dict:
        """Get order book for a symbol"""
        try:
            exchange_instance = self.exchanges.get(exchange)
            if not exchange_instance:
                raise ValueError(f"Exchange {exchange} not supported")
            
            order_book = exchange_instance.fetch_order_book(symbol, limit)
            
            return {
                'symbol': symbol,
                'exchange': exchange,
                'bids': [[Decimal(str(price)), Decimal(str(amount))] for price, amount in order_book['bids']],
                'asks': [[Decimal(str(price)), Decimal(str(amount))] for price, amount in order_book['asks']],
                'timestamp': timezone.now()
            }
        except Exception as e:
            logger.error(f"Error fetching order book for {symbol}: {str(e)}")
            return None
    
    def get_trading_pairs(self, exchange: str = 'binance') -> List[Dict]:
        """Get available trading pairs from exchange"""
        try:
            exchange_instance = self.exchanges.get(exchange)
            if not exchange_instance:
                raise ValueError(f"Exchange {exchange} not supported")
            
            markets = exchange_instance.load_markets()
            
            pairs = []
            for symbol, market in markets.items():
                if market['active']:
                    pairs.append({
                        'symbol': symbol,
                        'base': market['base'],
                        'quote': market['quote'],
                        'active': market['active'],
                        'precision': market['precision'],
                        'limits': market['limits']
                    })
            
            return pairs
        except Exception as e:
            logger.error(f"Error fetching trading pairs from {exchange}: {str(e)}")
            return []
    
    def store_market_data(self, symbol: str, data: List[Dict], exchange: str = 'binance'):
        """Store market data in database"""
        try:
            # Get or create exchange
            exchange_obj, created = Exchange.objects.get_or_create(
                code=exchange,
                defaults={'name': exchange.title(), 'api_url': f'https://{exchange}.com'}
            )
            
            # Get or create trading pair
            trading_pair, created = TradingPair.objects.get_or_create(
                exchange=exchange_obj,
                symbol=symbol,
                defaults={
                    'base_currency': symbol.split('/')[0],
                    'quote_currency': symbol.split('/')[1],
                    'is_active': True
                }
            )
            
            # Store market data
            market_data_objects = []
            for candle in data:
                market_data_objects.append(MarketData(
                    trading_pair=trading_pair,
                    timestamp=candle['timestamp'],
                    open_price=candle['open'],
                    high_price=candle['high'],
                    low_price=candle['low'],
                    close_price=candle['close'],
                    volume=candle['volume']
                ))
            
            MarketData.objects.bulk_create(market_data_objects, ignore_conflicts=True)
            logger.info(f"Stored {len(market_data_objects)} market data records for {symbol}")
            
        except Exception as e:
            logger.error(f"Error storing market data: {str(e)}")

class PriceAlertService:
    """Service for managing price alerts"""
    
    @staticmethod
    def create_alert(user, symbol: str, target_price: Decimal, condition: str, message: str = None):
        """Create a price alert"""
        alert = PriceAlert.objects.create(
            user=user,
            symbol=symbol,
            target_price=target_price,
            condition=condition,
            message=message or f"Price alert for {symbol} at {target_price}"
        )
        return alert
    
    @staticmethod
    def check_alerts(symbol: str, current_price: Decimal):
        """Check and trigger price alerts"""
        alerts = PriceAlert.objects.filter(
            symbol=symbol,
            is_triggered=False,
            is_active=True
        )
        
        triggered_alerts = []
        for alert in alerts:
            if alert.condition == 'above' and current_price >= alert.target_price:
                alert.trigger_alert()
                triggered_alerts.append(alert)
            elif alert.condition == 'below' and current_price <= alert.target_price:
                alert.trigger_alert()
                triggered_alerts.append(alert)
        
        return triggered_alerts

class TechnicalAnalysisService:
    """Service for technical analysis calculations"""
    
    @staticmethod
    def calculate_rsi(prices: List[Decimal], period: int = 14) -> List[Decimal]:
        """Calculate RSI (Relative Strength Index)"""
        if len(prices) < period + 1:
            return []
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [delta if delta > 0 else 0 for delta in deltas]
        losses = [-delta if delta < 0 else 0 for delta in deltas]
        
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        rsi_values = []
        for i in range(period, len(prices)):
            if avg_loss == 0:
                rsi_values.append(Decimal('100'))
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                rsi_values.append(Decimal(str(rsi)))
            
            # Update averages
            if i < len(prices) - 1:
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        return rsi_values
    
    @staticmethod
    def calculate_sma(prices: List[Decimal], period: int) -> List[Decimal]:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return []
        
        sma_values = []
        for i in range(period - 1, len(prices)):
            sma = sum(prices[i-period+1:i+1]) / period
            sma_values.append(sma)
        
        return sma_values
    
    @staticmethod
    def calculate_ema(prices: List[Decimal], period: int) -> List[Decimal]:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return []
        
        multiplier = 2 / (period + 1)
        ema_values = [sum(prices[:period]) / period]  # First EMA is SMA
        
        for price in prices[period:]:
            ema = (price * multiplier) + (ema_values[-1] * (1 - multiplier))
            ema_values.append(ema)
        
        return ema_values
