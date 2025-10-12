"""
Realistic price simulation with temporary profits before final outcome
"""
import random
import math
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone


class PricePathSimulator:
    """
    Generates realistic price paths that show temporary profits/losses
    but ultimately converge to the predetermined final outcome
    """
    
    def __init__(self, entry_price, target_percentage, duration_seconds, outcome='loss'):
        """
        Args:
            entry_price: Starting price
            target_percentage: Final profit/loss percentage (e.g., -80 for 80% loss)
            duration_seconds: Total trade duration
            outcome: 'win' or 'loss'
        """
        self.entry_price = float(entry_price)
        self.target_percentage = float(target_percentage)
        self.duration_seconds = duration_seconds
        self.outcome = outcome
        
        # Calculate final target price
        if outcome == 'win':
            self.target_price = self.entry_price * (1 + target_percentage / 100)
        else:
            self.target_price = self.entry_price * (1 - target_percentage / 100)
    
    def generate_price_path(self, num_points=50):
        """
        Generate a realistic price path with ups and downs
        
        Strategy:
        1. Show initial volatility (can go up or down)
        2. For LOSS trades: Show some temporary gains to give hope
        3. For WIN trades: Show some temporary dips to create suspense
        4. Gradually converge to target price as time approaches close
        5. Final point is exactly the target price
        
        Returns: List of (time_offset, price) tuples
        """
        price_path = []
        
        # Generate random walk that converges to target
        for i in range(num_points):
            progress = i / (num_points - 1)  # 0 to 1
            
            # Calculate base price (linear interpolation to target)
            base_price = self.entry_price + (self.target_price - self.entry_price) * progress
            
            # Add volatility that decreases over time
            # Early in trade: high volatility (can show opposite direction)
            # Late in trade: low volatility (converge to target)
            
            volatility_factor = (1 - progress) * 0.15  # Start with ±15%, decrease to 0
            
            # For LOSS trades: bias early movements upward (show temporary profits)
            if self.outcome == 'loss' and progress < 0.6:
                # Show temporary gains in first 60% of trade
                bias = 0.05 * (1 - progress)  # +5% bias early on
                noise = random.uniform(-volatility_factor, volatility_factor + bias)
            # For WIN trades: bias early movements downward (create suspense)
            elif self.outcome == 'win' and progress < 0.6:
                # Show temporary losses in first 60% of trade
                bias = 0.05 * (1 - progress)  # -5% bias early on
                noise = random.uniform(-volatility_factor - bias, volatility_factor)
            else:
                # In final 40%, converge smoothly to target
                noise = random.uniform(-volatility_factor, volatility_factor)
            
            price = base_price * (1 + noise)
            
            # Ensure price is always positive
            price = max(price, self.entry_price * 0.01)
            
            # For last point, ensure exact target
            if i == num_points - 1:
                price = self.target_price
            
            # Time offset in seconds
            time_offset = int((progress * self.duration_seconds))
            
            price_path.append((time_offset, price))
        
        return price_path
    
    def get_current_price(self, elapsed_seconds):
        """
        Get the current price based on elapsed time
        Interpolates along the generated price path
        """
        # Generate path if not already generated
        if not hasattr(self, '_price_path'):
            self._price_path = self.generate_price_path()
        
        # Find the appropriate price for current time
        progress = min(elapsed_seconds / self.duration_seconds, 1.0)
        
        # Calculate with realistic movement
        base_price = self.entry_price + (self.target_price - self.entry_price) * progress
        
        # Add some random noise
        volatility = (1 - progress) * 0.05  # Decreasing volatility
        
        if self.outcome == 'loss' and progress < 0.7:
            # Show temporary gains
            bias = 0.03 * (1 - progress)
            noise = random.uniform(-volatility, volatility + bias)
        elif self.outcome == 'win' and progress < 0.7:
            # Show temporary losses  
            bias = 0.03 * (1 - progress)
            noise = random.uniform(-volatility - bias, volatility)
        else:
            # Converge to target
            noise = random.uniform(-volatility / 2, volatility / 2)
        
        current_price = base_price * (1 + noise)
        
        # Ensure convergence at the end
        if progress >= 0.95:
            # Last 5%, force convergence to target
            current_price = self.target_price + (current_price - self.target_price) * (1 - progress) * 20
        
        return max(current_price, self.entry_price * 0.01)
    
    def generate_candlestick_data(self, interval_seconds=300):
        """
        Generate candlestick data (OHLCV) for the entire trade period
        
        Args:
            interval_seconds: Candlestick interval (e.g., 300 for 5-minute candles)
        
        Returns: List of candlestick dicts
        """
        num_candles = max(1, self.duration_seconds // interval_seconds)
        candles = []
        
        for i in range(num_candles):
            start_time = i * interval_seconds
            end_time = min((i + 1) * interval_seconds, self.duration_seconds)
            
            # Get prices at start and end
            start_progress = start_time / self.duration_seconds
            end_progress = end_time / self.duration_seconds
            
            # Calculate open and close prices
            open_price = self._get_price_at_progress(start_progress)
            close_price = self._get_price_at_progress(end_progress)
            
            # Calculate high and low with some randomness
            high_price = max(open_price, close_price) * random.uniform(1.0, 1.02)
            low_price = min(open_price, close_price) * random.uniform(0.98, 1.0)
            
            # Volume
            volume = random.uniform(100000, 500000)
            
            candles.append({
                'timestamp': start_time,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume
            })
        
        return candles
    
    def _get_price_at_progress(self, progress):
        """Helper to get price at a specific progress point (0 to 1)"""
        base_price = self.entry_price + (self.target_price - self.entry_price) * progress
        volatility = (1 - progress) * 0.05
        
        if self.outcome == 'loss' and progress < 0.7:
            bias = 0.03 * (1 - progress)
            noise = random.uniform(-volatility, volatility + bias)
        elif self.outcome == 'win' and progress < 0.7:
            bias = 0.03 * (1 - progress)
            noise = random.uniform(-volatility - bias, volatility)
        else:
            noise = random.uniform(-volatility / 2, volatility / 2)
        
        current_price = base_price * (1 + noise)
        
        if progress >= 0.95:
            current_price = self.target_price + (current_price - self.target_price) * (1 - progress) * 20
        
        return max(current_price, self.entry_price * 0.01)


class ActiveTradeManager:
    """
    Manages active trades and their price simulations
    """
    
    @staticmethod
    def get_active_trade_simulator(trade_outcome):
        """
        Get or create a price simulator for an active trade outcome
        
        Args:
            trade_outcome: UserTradeOutcome instance
        
        Returns: PricePathSimulator instance
        """
        if not trade_outcome.trade:
            return None
        
        entry_price = float(trade_outcome.trade.price)
        target_percentage = float(trade_outcome.outcome_percentage)
        
        # Calculate remaining duration
        now = timezone.now()
        total_duration = trade_outcome.duration_seconds
        
        if trade_outcome.target_close_time > now:
            # Calculate elapsed time
            elapsed = (now - trade_outcome.trade.executed_at).total_seconds()
            remaining = (trade_outcome.target_close_time - now).total_seconds()
            
            # Create simulator
            simulator = PricePathSimulator(
                entry_price=entry_price,
                target_percentage=target_percentage,
                duration_seconds=total_duration,
                outcome=trade_outcome.outcome
            )
            
            return simulator, elapsed
        
        return None, 0
    
    @staticmethod
    def get_current_simulated_price(trade_outcome):
        """
        Get the current simulated price for an active trade
        Includes realistic movements but converges to target
        """
        result = ActiveTradeManager.get_active_trade_simulator(trade_outcome)
        
        if not result or result[0] is None:
            return None
        
        simulator, elapsed = result
        current_price = simulator.get_current_price(elapsed)
        
        return Decimal(str(current_price))

