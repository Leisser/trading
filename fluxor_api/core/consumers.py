import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

logger = logging.getLogger(__name__)

class PriceConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time price updates"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        try:
            # Get user from scope
            self.user = self.scope.get('user', AnonymousUser())
            
            if not self.user.is_authenticated:
                await self.close()
                return
            
            # Accept connection
            await self.accept()
            
            # Add to price updates group
            await self.channel_layer.group_add(
                'price_updates',
                self.channel_name
            )
            
            logger.info(f"Price consumer connected for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error in price consumer connect: {str(e)}")
            await self.close()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        try:
            # Remove from price updates group
            await self.channel_layer.group_discard(
                'price_updates',
                self.channel_name
            )
            
            logger.info(f"Price consumer disconnected for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error in price consumer disconnect: {str(e)}")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'subscribe':
                # Subscribe to specific trading pairs
                trading_pairs = data.get('trading_pairs', [])
                await self.subscribe_to_pairs(trading_pairs)
            
            elif message_type == 'unsubscribe':
                # Unsubscribe from specific trading pairs
                trading_pairs = data.get('trading_pairs', [])
                await self.unsubscribe_from_pairs(trading_pairs)
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error in price consumer receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Internal server error'
            }))
    
    async def subscribe_to_pairs(self, trading_pairs):
        """Subscribe to specific trading pairs"""
        try:
            for pair in trading_pairs:
                group_name = f"price_{pair}"
                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name
                )
            
            await self.send(text_data=json.dumps({
                'type': 'subscription_confirmed',
                'trading_pairs': trading_pairs
            }))
            
        except Exception as e:
            logger.error(f"Error subscribing to pairs: {str(e)}")
    
    async def unsubscribe_from_pairs(self, trading_pairs):
        """Unsubscribe from specific trading pairs"""
        try:
            for pair in trading_pairs:
                group_name = f"price_{pair}"
                await self.channel_layer.group_discard(
                    group_name,
                    self.channel_name
                )
            
            await self.send(text_data=json.dumps({
                'type': 'unsubscription_confirmed',
                'trading_pairs': trading_pairs
            }))
            
        except Exception as e:
            logger.error(f"Error unsubscribing from pairs: {str(e)}")
    
    async def price_update(self, event):
        """Handle price update events"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'price_update',
                'trading_pair': event['trading_pair'],
                'price': event['price'],
                'timestamp': event['timestamp'],
                'change_24h': event.get('change_24h'),
                'volume': event.get('volume'),
            }))
            
        except Exception as e:
            logger.error(f"Error sending price update: {str(e)}")

class TradingConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for trading updates"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        try:
            # Get user from scope
            self.user = self.scope.get('user', AnonymousUser())
            
            if not self.user.is_authenticated:
                await self.close()
                return
            
            # Accept connection
            await self.accept()
            
            # Add to user-specific trading group
            await self.channel_layer.group_add(
                f"trading_{self.user.id}",
                self.channel_name
            )
            
            logger.info(f"Trading consumer connected for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error in trading consumer connect: {str(e)}")
            await self.close()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        try:
            # Remove from trading group
            await self.channel_layer.group_discard(
                f"trading_{self.user.id}",
                self.channel_name
            )
            
            logger.info(f"Trading consumer disconnected for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error in trading consumer disconnect: {str(e)}")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'order_status':
                # Get order status
                order_id = data.get('order_id')
                await self.get_order_status(order_id)
            
            elif message_type == 'portfolio_update':
                # Get portfolio update
                await self.get_portfolio_update()
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error in trading consumer receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Internal server error'
            }))
    
    async def get_order_status(self, order_id):
        """Get order status"""
        try:
            order_data = await self.get_order_data(order_id)
            await self.send(text_data=json.dumps({
                'type': 'order_status',
                'order': order_data
            }))
            
        except Exception as e:
            logger.error(f"Error getting order status: {str(e)}")
    
    async def get_portfolio_update(self):
        """Get portfolio update"""
        try:
            portfolio_data = await self.get_portfolio_data()
            await self.send(text_data=json.dumps({
                'type': 'portfolio_update',
                'portfolio': portfolio_data
            }))
            
        except Exception as e:
            logger.error(f"Error getting portfolio update: {str(e)}")
    
    @database_sync_to_async
    def get_order_data(self, order_id):
        """Get order data from database"""
        from order_management.models import Order
        
        try:
            order = Order.objects.get(id=order_id, user=self.user)
            return {
                'id': order.id,
                'trading_pair': f"{order.trading_pair.base_currency.symbol}/{order.trading_pair.quote_currency.symbol}",
                'order_type': order.order_type,
                'side': order.side,
                'amount': float(order.amount),
                'price': float(order.price) if order.price else None,
                'status': order.status,
                'filled_amount': float(order.filled_amount) if order.filled_amount else 0,
                'created_at': order.created_at.isoformat(),
            }
        except Order.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_portfolio_data(self):
        """Get portfolio data from database"""
        from portfolio_management.models import Portfolio, Position
        
        try:
            portfolio = Portfolio.objects.get(user=self.user)
            positions = Position.objects.filter(user=self.user)
            
            position_data = []
            for position in positions:
                position_data.append({
                    'trading_pair': f"{position.trading_pair.base_currency.symbol}/{position.trading_pair.quote_currency.symbol}",
                    'amount': float(position.amount),
                    'current_value': float(position.current_value) if position.current_value else 0,
                    'unrealized_pnl': float(position.unrealized_pnl) if position.unrealized_pnl else 0,
                })
            
            return {
                'total_value': float(portfolio.total_value),
                'positions_value': float(portfolio.positions_value),
                'cash_value': float(portfolio.cash_value),
                'positions': position_data,
            }
        except Portfolio.DoesNotExist:
            return None
    
    async def order_update(self, event):
        """Handle order update events"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'order_update',
                'order_id': event['order_id'],
                'status': event['status'],
                'filled_amount': event.get('filled_amount'),
                'timestamp': event['timestamp'],
            }))
            
        except Exception as e:
            logger.error(f"Error sending order update: {str(e)}")
    
    async def trade_executed(self, event):
        """Handle trade execution events"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'trade_executed',
                'trade_id': event['trade_id'],
                'trading_pair': event['trading_pair'],
                'side': event['side'],
                'amount': event['amount'],
                'price': event['price'],
                'timestamp': event['timestamp'],
            }))
            
        except Exception as e:
            logger.error(f"Error sending trade executed: {str(e)}")

class AlertConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for alerts and notifications"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        try:
            # Get user from scope
            self.user = self.scope.get('user', AnonymousUser())
            
            if not self.user.is_authenticated:
                await self.close()
                return
            
            # Accept connection
            await self.accept()
            
            # Add to user-specific alert group
            await self.channel_layer.group_add(
                f"user_{self.user.id}",
                self.channel_name
            )
            
            logger.info(f"Alert consumer connected for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error in alert consumer connect: {str(e)}")
            await self.close()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        try:
            # Remove from alert group
            await self.channel_layer.group_discard(
                f"user_{self.user.id}",
                self.channel_name
            )
            
            logger.info(f"Alert consumer disconnected for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error in alert consumer disconnect: {str(e)}")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'mark_read':
                # Mark alert as read
                alert_id = data.get('alert_id')
                await self.mark_alert_read(alert_id)
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error in alert consumer receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Internal server error'
            }))
    
    async def mark_alert_read(self, alert_id):
        """Mark alert as read"""
        try:
            success = await self.mark_alert_read_db(alert_id)
            await self.send(text_data=json.dumps({
                'type': 'alert_marked_read',
                'alert_id': alert_id,
                'success': success
            }))
            
        except Exception as e:
            logger.error(f"Error marking alert read: {str(e)}")
    
    @database_sync_to_async
    def mark_alert_read_db(self, alert_id):
        """Mark alert as read in database"""
        from alerts.models import Alert
        
        try:
            alert = Alert.objects.get(id=alert_id, user=self.user)
            alert.read_at = timezone.now()
            alert.save()
            return True
        except Alert.DoesNotExist:
            return False
    
    async def alert_notification(self, event):
        """Handle alert notification events"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'alert_notification',
                'alert_id': event['alert_id'],
                'title': event.get('title'),
                'message': event.get('message'),
                'severity': event.get('severity'),
                'timestamp': event.get('timestamp'),
            }))
            
        except Exception as e:
            logger.error(f"Error sending alert notification: {str(e)}")

class MarketDataConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for market data updates"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        try:
            # Get user from scope
            self.user = self.scope.get('user', AnonymousUser())
            
            if not self.user.is_authenticated:
                await self.close()
                return
            
            # Accept connection
            await self.accept()
            
            # Add to market data group
            await self.channel_layer.group_add(
                'market_data',
                self.channel_name
            )
            
            logger.info(f"Market data consumer connected for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error in market data consumer connect: {str(e)}")
            await self.close()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        try:
            # Remove from market data group
            await self.channel_layer.group_discard(
                'market_data',
                self.channel_name
            )
            
            logger.info(f"Market data consumer disconnected for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error in market data consumer disconnect: {str(e)}")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'subscribe_orderbook':
                # Subscribe to order book updates
                trading_pair = data.get('trading_pair')
                await self.subscribe_to_orderbook(trading_pair)
            
            elif message_type == 'subscribe_trades':
                # Subscribe to trade updates
                trading_pair = data.get('trading_pair')
                await self.subscribe_to_trades(trading_pair)
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error in market data consumer receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Internal server error'
            }))
    
    async def subscribe_to_orderbook(self, trading_pair):
        """Subscribe to order book updates"""
        try:
            group_name = f"orderbook_{trading_pair}"
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )
            
            await self.send(text_data=json.dumps({
                'type': 'orderbook_subscription_confirmed',
                'trading_pair': trading_pair
            }))
            
        except Exception as e:
            logger.error(f"Error subscribing to orderbook: {str(e)}")
    
    async def subscribe_to_trades(self, trading_pair):
        """Subscribe to trade updates"""
        try:
            group_name = f"trades_{trading_pair}"
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )
            
            await self.send(text_data=json.dumps({
                'type': 'trades_subscription_confirmed',
                'trading_pair': trading_pair
            }))
            
        except Exception as e:
            logger.error(f"Error subscribing to trades: {str(e)}")
    
    async def orderbook_update(self, event):
        """Handle order book update events"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'orderbook_update',
                'trading_pair': event['trading_pair'],
                'bids': event['bids'],
                'asks': event['asks'],
                'timestamp': event['timestamp'],
            }))
            
        except Exception as e:
            logger.error(f"Error sending orderbook update: {str(e)}")
    
    async def trade_update(self, event):
        """Handle trade update events"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'trade_update',
                'trading_pair': event['trading_pair'],
                'price': event['price'],
                'amount': event['amount'],
                'side': event['side'],
                'timestamp': event['timestamp'],
            }))
            
        except Exception as e:
            logger.error(f"Error sending trade update: {str(e)}") 