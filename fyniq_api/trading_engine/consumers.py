import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import asyncio
import ccxt
from pycoingecko import CoinGeckoAPI

class PriceFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.exchange = ccxt.binance()
        self.coingecko = CoinGeckoAPI()
        self.running = True
        asyncio.create_task(self.send_price_updates())

    async def disconnect(self, close_code):
        self.running = False

    async def send_price_updates(self):
        while self.running:
            try:
                # Get BTC/USD price from Binance
                ticker = await sync_to_async(self.exchange.fetch_ticker)("BTC/USDT")
                price = ticker['last']
                # Get BTC/USD price from CoinGecko as backup
                cg_price = await sync_to_async(self.coingecko.get_price)(ids='bitcoin', vs_currencies='usd')
                cg_price = cg_price['bitcoin']['usd']
                await self.send(json.dumps({
                    'binance': price,
                    'coingecko': cg_price
                }))
            except Exception as e:
                await self.send(json.dumps({'error': str(e)}))
            await asyncio.sleep(5)

class TradeUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # In a real system, subscribe to user-specific trade updates
        await self.send(json.dumps({'message': 'Connected to trade updates'}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Echo for now
        await self.send(text_data) 