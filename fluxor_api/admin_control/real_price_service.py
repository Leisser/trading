"""
Real-time cryptocurrency price fetching service
Integrates with CoinGecko API and CCXT for live market data
"""
import ccxt
from pycoingecko import CoinGeckoAPI
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class RealPriceService:
    """Service to fetch real cryptocurrency prices from external APIs"""
    
    # CoinGecko API mapping
    COINGECKO_IDS = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'USDT': 'tether',
        'BNB': 'binancecoin',
        'SOL': 'solana',
        'XRP': 'ripple',
        'ADA': 'cardano',
        'DOGE': 'dogecoin',
        'TRX': 'tron',
        'DOT': 'polkadot',
        'MATIC': 'matic-network',
        'LTC': 'litecoin',
        'AVAX': 'avalanche-2',
        'LINK': 'chainlink',
        'UNI': 'uniswap',
    }
    
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.exchange = None
        try:
            # Initialize Binance exchange (public data, no API key needed)
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
            })
        except Exception as e:
            logger.warning(f"Failed to initialize CCXT exchange: {e}")
    
    def get_current_price(self, symbol='BTC'):
        """
        Get current price for a cryptocurrency
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        
        Returns:
            float: Current price in USD
        """
        # Try cache first (60 second TTL)
        cache_key = f'real_price_{symbol}'
        try:
            cached_price = cache.get(cache_key)
            if cached_price:
                return float(cached_price)
        except:
            # Cache not configured, continue without caching
            pass
        
        try:
            # Try CCXT first (faster)
            if self.exchange:
                ticker = self.exchange.fetch_ticker(f'{symbol}/USDT')
                price = float(ticker['last'])
                try:
                    cache.set(cache_key, price, 60)  # Cache for 60 seconds
                except:
                    pass
                return price
        except Exception as e:
            logger.debug(f"CCXT fetch failed for {symbol}: {e}")
        
        try:
            # Fallback to CoinGecko
            coin_id = self.COINGECKO_IDS.get(symbol)
            if coin_id:
                data = self.cg.get_price(ids=coin_id, vs_currencies='usd')
                price = float(data[coin_id]['usd'])
                try:
                    cache.set(cache_key, price, 60)
                except:
                    pass
                return price
        except Exception as e:
            logger.error(f"CoinGecko fetch failed for {symbol}: {e}")
        
        # If all fails, return None
        return None
    
    def get_historical_data(self, symbol='BTC', days=1, interval='hourly'):
        """
        Get historical OHLCV data
        
        Args:
            symbol: Cryptocurrency symbol
            days: Number of days of history
            interval: 'minutely' | 'hourly' | 'daily'
        
        Returns:
            list: List of OHLCV candles
        """
        try:
            # Use CCXT for OHLCV data
            if self.exchange:
                # Determine timeframe
                if interval == 'minutely':
                    timeframe = '1m'
                    limit = days * 24 * 60
                elif interval == 'hourly':
                    timeframe = '1h'
                    limit = days * 24
                else:  # daily
                    timeframe = '1d'
                    limit = days
                
                # Limit to reasonable amounts
                limit = min(limit, 1000)
                
                ohlcv = self.exchange.fetch_ohlcv(
                    f'{symbol}/USDT',
                    timeframe=timeframe,
                    limit=limit
                )
                
                candles = []
                for candle in ohlcv:
                    timestamp, open_p, high, low, close, volume = candle
                    candles.append({
                        'timestamp': timestamp // 1000,  # Convert to seconds
                        'open': float(open_p),
                        'high': float(high),
                        'low': float(low),
                        'close': float(close),
                        'volume': float(volume)
                    })
                
                return candles
        except Exception as e:
            logger.error(f"Failed to fetch historical data for {symbol}: {e}")
        
        # Fallback: Try CoinGecko market chart
        try:
            coin_id = self.COINGECKO_IDS.get(symbol)
            if coin_id:
                data = self.cg.get_coin_market_chart_by_id(
                    id=coin_id,
                    vs_currency='usd',
                    days=days
                )
                
                # CoinGecko returns price points, convert to candles
                prices = data.get('prices', [])
                candles = []
                
                # Group by hour (simplified OHLC)
                for i in range(0, len(prices) - 4, 4):
                    segment = prices[i:i+4]
                    if len(segment) >= 4:
                        timestamp = segment[0][0] // 1000
                        values = [p[1] for p in segment]
                        candles.append({
                            'timestamp': timestamp,
                            'open': float(values[0]),
                            'high': float(max(values)),
                            'low': float(min(values)),
                            'close': float(values[-1]),
                            'volume': 0  # CoinGecko doesn't provide volume in this format
                        })
                
                return candles
        except Exception as e:
            logger.error(f"CoinGecko historical data failed for {symbol}: {e}")
        
        return []
    
    def get_multiple_prices(self, symbols):
        """
        Get current prices for multiple cryptocurrencies at once
        
        Args:
            symbols: List of symbols ['BTC', 'ETH', ...]
        
        Returns:
            dict: {symbol: price}
        """
        prices = {}
        
        try:
            # Build CoinGecko IDs list
            coin_ids = []
            id_to_symbol = {}
            for symbol in symbols:
                coin_id = self.COINGECKO_IDS.get(symbol)
                if coin_id:
                    coin_ids.append(coin_id)
                    id_to_symbol[coin_id] = symbol
            
            # Fetch all at once
            if coin_ids:
                data = self.cg.get_price(ids=','.join(coin_ids), vs_currencies='usd')
                for coin_id, price_data in data.items():
                    symbol = id_to_symbol.get(coin_id)
                    if symbol:
                        prices[symbol] = float(price_data['usd'])
        except Exception as e:
            logger.error(f"Failed to fetch multiple prices: {e}")
            # Fallback to individual fetches
            for symbol in symbols:
                price = self.get_current_price(symbol)
                if price:
                    prices[symbol] = price
        
        return prices
    
    def get_24h_stats(self, symbol='BTC'):
        """
        Get 24-hour statistics (change, volume, etc.)
        
        Args:
            symbol: Cryptocurrency symbol
        
        Returns:
            dict: Statistics including price_change_24h, volume_24h
        """
        try:
            if self.exchange:
                ticker = self.exchange.fetch_ticker(f'{symbol}/USDT')
                return {
                    'price': float(ticker.get('last', 0)),
                    'price_change_24h': float(ticker.get('percentage', 0)),
                    'high_24h': float(ticker.get('high', 0)),
                    'low_24h': float(ticker.get('low', 0)),
                    'volume_24h': float(ticker.get('quoteVolume', 0)),
                }
        except Exception as e:
            logger.error(f"Failed to fetch 24h stats for {symbol}: {e}")
        
        try:
            coin_id = self.COINGECKO_IDS.get(symbol)
            if coin_id:
                data = self.cg.get_coin_by_id(id=coin_id)
                market_data = data.get('market_data', {})
                return {
                    'price': float(market_data.get('current_price', {}).get('usd', 0)),
                    'price_change_24h': float(market_data.get('price_change_percentage_24h', 0)),
                    'high_24h': float(market_data.get('high_24h', {}).get('usd', 0)),
                    'low_24h': float(market_data.get('low_24h', {}).get('usd', 0)),
                    'volume_24h': float(market_data.get('total_volume', {}).get('usd', 0)),
                }
        except Exception as e:
            logger.error(f"CoinGecko 24h stats failed for {symbol}: {e}")
        
        return {}
    
    def is_available(self):
        """Check if the service is working"""
        try:
            price = self.get_current_price('BTC')
            return price is not None
        except:
            return False


# Singleton instance
_service_instance = None

def get_price_service():
    """Get or create the price service singleton"""
    global _service_instance
    if _service_instance is None:
        _service_instance = RealPriceService()
    return _service_instance

