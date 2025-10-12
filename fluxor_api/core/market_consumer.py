"""
WebSocket consumer for real-time market data streaming
"""
import json
import asyncio
import random
from decimal import Decimal
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class MarketDataConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for streaming live market data
    Sends real-time price updates for candlestick and line charts
    """
    
    async def connect(self):
        self.cryptocurrency_symbol = self.scope['url_route']['kwargs'].get('symbol', 'BTC')
        self.room_group_name = f'market_{self.cryptocurrency_symbol}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Start sending market data
        asyncio.create_task(self.send_market_updates())
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            action = data.get('action')
            
            if action == 'subscribe':
                # Subscribe to different cryptocurrency
                new_symbol = data.get('symbol', 'BTC')
                if new_symbol != self.cryptocurrency_symbol:
                    # Leave old group
                    await self.channel_layer.group_discard(
                        self.room_group_name,
                        self.channel_name
                    )
                    
                    # Join new group
                    self.cryptocurrency_symbol = new_symbol
                    self.room_group_name = f'market_{self.cryptocurrency_symbol}'
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
                    
                    await self.send(text_data=json.dumps({
                        'type': 'subscription_changed',
                        'symbol': new_symbol
                    }))
        
        except json.JSONDecodeError:
            pass
    
    async def send_market_updates(self):
        """Continuously send market data updates"""
        while True:
            try:
                # Get trading settings for update interval
                settings = await self.get_trading_settings()
                update_interval = settings.get('update_interval_seconds', 5)
                volatility = settings.get('price_volatility_percentage', 2.0)
                
                # Get current price
                current_price = await self.get_current_price(self.cryptocurrency_symbol)
                
                # Generate simulated price data
                market_data = await self.generate_market_data(
                    self.cryptocurrency_symbol,
                    current_price,
                    volatility
                )
                
                # Send to WebSocket
                await self.send(text_data=json.dumps({
                    'type': 'market_update',
                    'symbol': self.cryptocurrency_symbol,
                    'timestamp': market_data['timestamp'],
                    'price': market_data['close'],
                    'open': market_data['open'],
                    'high': market_data['high'],
                    'low': market_data['low'],
                    'close': market_data['close'],
                    'volume': market_data['volume'],
                    'change_24h': market_data['change_24h']
                }))
                
                # Wait before next update
                await asyncio.sleep(update_interval)
            
            except Exception as e:
                print(f"Error in market updates: {e}")
                await asyncio.sleep(5)
    
    @database_sync_to_async
    def get_trading_settings(self):
        """Get admin trading settings"""
        from admin_control.models import TradingSettings
        settings = TradingSettings.get_active_settings()
        return {
            'update_interval_seconds': settings.update_interval_seconds,
            'price_volatility_percentage': float(settings.price_volatility_percentage)
        }
    
    @database_sync_to_async
    def get_current_price(self, symbol):
        """Get current cryptocurrency price"""
        from trades.models import Cryptocurrency
        try:
            crypto = Cryptocurrency.objects.get(symbol=symbol)
            return float(crypto.current_price)
        except Cryptocurrency.DoesNotExist:
            return 43250.0  # Default BTC price
    
    @database_sync_to_async
    def generate_market_data(self, symbol, base_price, volatility_percent):
        """
        Generate simulated market data with volatility
        For active trades, follows predetermined price path with realistic movements
        """
        from admin_control.models import MarketDataSimulation, UserTradeOutcome
        from admin_control.price_simulator import ActiveTradeManager
        from trades.models import Cryptocurrency
        
        # Check if there are active trades for this cryptocurrency
        active_outcomes = UserTradeOutcome.objects.filter(
            is_executed=False,
            trade__cryptocurrency__symbol=symbol,
            trade__trade_type='buy'
        ).select_related('trade').order_by('created_at')
        
        if active_outcomes.exists():
            # Use the oldest active trade to determine price movement
            oldest_outcome = active_outcomes.first()
            simulated_price = ActiveTradeManager.get_current_simulated_price(oldest_outcome)
            
            if simulated_price:
                # Generate OHLC based on simulated price path
                volatility = float(volatility_percent) / 100
                close_price = simulated_price
                
                # Add small random fluctuations within the candle
                open_price = close_price * Decimal(str(random.uniform(0.998, 1.002)))
                high_price = max(open_price, close_price) * Decimal(str(random.uniform(1.0, 1.005)))
                low_price = min(open_price, close_price) * Decimal(str(random.uniform(0.995, 1.0)))
                volume = Decimal(str(random.uniform(100000, 1000000)))
                
                # Update cryptocurrency price in database
                try:
                    crypto = Cryptocurrency.objects.get(symbol=symbol)
                    crypto.current_price = close_price
                    crypto.save(update_fields=['current_price'])
                except Cryptocurrency.DoesNotExist:
                    pass
                
                # Calculate change from entry
                entry_price = float(oldest_outcome.trade.price)
                change_from_entry = ((float(close_price) - entry_price) / entry_price) * 100
                
                # Save to market simulation
                sim_data = MarketDataSimulation.objects.create(
                    cryptocurrency_symbol=symbol,
                    open_price=open_price,
                    high_price=high_price,
                    low_price=low_price,
                    close_price=close_price,
                    volume=volume
                )
                
                return {
                    'timestamp': sim_data.timestamp.isoformat(),
                    'open': float(open_price),
                    'high': float(high_price),
                    'low': float(low_price),
                    'close': float(close_price),
                    'volume': float(volume),
                    'change_24h': change_from_entry,  # Show change from entry price
                    'trade_active': True
                }
        
        # No active trades - use normal random walk
        volatility = float(volatility_percent) / 100
        price_change_factor = random.uniform(-volatility, volatility)
        
        # Generate OHLC data
        open_price = Decimal(str(base_price))
        close_price = open_price * Decimal(str(1 + price_change_factor))
        high_price = max(open_price, close_price) * Decimal(str(1 + abs(price_change_factor) / 2))
        low_price = min(open_price, close_price) * Decimal(str(1 - abs(price_change_factor) / 2))
        volume = Decimal(str(random.uniform(100000, 1000000)))
        
        # Update cryptocurrency price in database
        try:
            crypto = Cryptocurrency.objects.get(symbol=symbol)
            crypto.current_price = close_price
            crypto.save(update_fields=['current_price'])
        except Cryptocurrency.DoesNotExist:
            pass
        
        # Save to market simulation
        sim_data = MarketDataSimulation.objects.create(
            cryptocurrency_symbol=symbol,
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            close_price=close_price,
            volume=volume
        )
        
        # Calculate 24h change (mock)
        change_24h = random.uniform(-5.0, 5.0)
        
        return {
            'timestamp': sim_data.timestamp.isoformat(),
            'open': float(open_price),
            'high': float(high_price),
            'low': float(low_price),
            'close': float(close_price),
            'volume': float(volume),
            'change_24h': change_24h,
            'trade_active': False
        }
    
    # Handle group messages
    async def market_update(self, event):
        """Receive market update from group"""
        await self.send(text_data=json.dumps(event['data']))

