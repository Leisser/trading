import pandas as pd
import ta
import ccxt

class TradingAlgorithmService:
    def __init__(self, symbol="BTC/USDT", timeframe="1m"):
        self.symbol = symbol
        self.timeframe = timeframe
        self.exchange = ccxt.binance()

    def fetch_ohlcv(self, limit=100):
        ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df

    def compute_indicators(self, df):
        df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
        df["sma"] = ta.trend.SMAIndicator(df["close"], window=14).sma_indicator()
        df["ema"] = ta.trend.EMAIndicator(df["close"], window=14).ema_indicator()
        return df

    def generate_signal(self, df):
        # Example: simple RSI strategy
        if df["rsi"].iloc[-1] < 30:
            return "buy"
        elif df["rsi"].iloc[-1] > 70:
            return "sell"
        else:
            return "hold"

    def run_strategy(self):
        df = self.fetch_ohlcv()
        df = self.compute_indicators(df)
        signal = self.generate_signal(df)
        return signal 