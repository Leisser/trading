"""
WebSocket consumers for real-time trade updates
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from decimal import Decimal


class TradeUpdateConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time trade updates.
    Sends trade_sum updates and status changes to connected clients.
    """
    
    async def connect(self):
        self.user = self.scope.get("user")
        
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        
        # Create user-specific group
        self.user_group_name = f'trades_user_{self.user.id}'
        
        # Join user group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to trade updates'
        }))
    
    async def disconnect(self, close_code):
        # Leave user group
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong'
                }))
        except json.JSONDecodeError:
            pass
    
    async def trade_update(self, event):
        """
        Handle trade update messages from the group.
        Sends trade_sum updates to the client.
        """
        await self.send(text_data=json.dumps({
            'type': 'trade_update',
            'trade_id': event['trade_id'],
            'trade_sum': str(event['trade_sum']),
            'current_price': str(event.get('current_price', 0)),
            'pnl': str(event.get('pnl', 0)),
            'status': event.get('status', 'active'),
            'timestamp': event.get('timestamp', '')
        }))
    
    async def trade_completed(self, event):
        """
        Handle trade completion messages.
        Notifies client when trade_sum reaches zero.
        """
        await self.send(text_data=json.dumps({
            'type': 'trade_completed',
            'trade_id': event['trade_id'],
            'final_pnl': str(event.get('final_pnl', 0)),
            'timestamp': event.get('timestamp', '')
        }))
    
    async def balance_update(self, event):
        """
        Handle balance update messages.
        Notifies client when balance changes (e.g., trade stopped).
        """
        await self.send(text_data=json.dumps({
            'type': 'balance_update',
            'balance': str(event['balance']),
            'currency': event.get('currency', 'USDT'),
            'reason': event.get('reason', 'trade_stopped'),
            'amount_returned': str(event.get('amount_returned', 0)),
            'timestamp': event.get('timestamp', '')
        }))

