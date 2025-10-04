"""
WebSocket consumers for Fluxor API.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


class TradingConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for trading operations."""
    
    async def connect(self):
        """Accept WebSocket connection."""
        self.room_group_name = 'trading_room'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'trading_message',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))

    async def trading_message(self, event):
        """Send message to WebSocket."""
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


class MarketDataConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for market data."""
    
    async def connect(self):
        """Accept WebSocket connection."""
        self.room_group_name = 'market_data_room'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'market_data_message',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))

    async def market_data_message(self, event):
        """Send message to WebSocket."""
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for notifications."""
    
    async def connect(self):
        """Accept WebSocket connection."""
        self.room_group_name = 'notifications_room'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))

    async def notification_message(self, event):
        """Send message to WebSocket."""
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
