#!/usr/bin/env python3
"""
Enhanced Trading Tasks Management Command
Handles automated trading tasks for all 200+ cryptocurrencies
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import time
import random
import logging
import json
from datetime import timedelta
from trades.models import (
    Cryptocurrency, Trade, PriceData, TradingSignal, 
    CryptoInvestment, TradingSettings, ProfitLossScenario,
    PriceMovementLog, AutomatedTask
)
from django.contrib.auth import get_user_model

User = get_user_model()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run automated trading tasks for all cryptocurrencies'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_counter = 0
        self.crypto_rotation_index = 0
        self.last_full_update = timezone.now()

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=5,
            help='Update interval in seconds (default: 5)',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=20,
            help='Number of cryptocurrencies to update per batch (default: 20)',
        )
        parser.add_argument(
            '--simulate-trades',
            action='store_true',
            help='Simulate actual trading activity',
        )
        parser.add_argument(
            '--enable-scenarios',
            action='store_true',
            help='Execute profit/loss scenarios',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose logging',
        )

    def handle(self, *args, **options):
        self.interval = options['interval']
        self.batch_size = options['batch_size']
        self.simulate_trades = options['simulate_trades']
        self.enable_scenarios = options['enable_scenarios']
        self.verbose = options['verbose']

        self.stdout.write(
            self.style.SUCCESS('🚀 Starting Enhanced Trading Tasks System')
        )
        self.stdout.write(f"   • Update Interval: {self.interval} seconds")
        self.stdout.write(f"   • Batch Size: {self.batch_size} cryptocurrencies")
        self.stdout.write(f"   • Simulate Trades: {'Yes' if self.simulate_trades else 'No'}")
        self.stdout.write(f"   • Scenarios Enabled: {'Yes' if self.enable_scenarios else 'No'}")
        
        # Get trading settings
        settings = self.get_or_create_settings()
        self.stdout.write(f"   • Trading Enabled: {'Yes' if settings.trading_enabled else 'No'}")
        
        if settings.maintenance_mode:
            self.stdout.write(
                self.style.WARNING('⚠️  System is in maintenance mode - tasks will run but with limited functionality')
            )

        # Main loop
        try:
            while True:
                self.run_task_cycle()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.SUCCESS('\n✅ Trading tasks stopped by user')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Trading tasks stopped due to error: {str(e)}')
            )
            logger.exception("Trading tasks error")

    def run_task_cycle(self):
        """Run one complete task cycle"""
        self.task_counter += 1
        start_time = timezone.now()
        
        if self.verbose:
            self.stdout.write(f"\n🔄 Task Cycle #{self.task_counter} - {start_time.strftime('%H:%M:%S')}")

        # Create automated task record
        task = AutomatedTask.objects.create(
            task_type='price_update',
            task_name=f'Cycle #{self.task_counter} - Multi-Crypto Update',
            status='running',
            started_at=start_time
        )

        try:
            # 1. Update cryptocurrency prices (batch rotation)
            updated_count = self.update_crypto_prices_batch()
            
            # 2. Generate trading signals
            signals_generated = self.generate_trading_signals()
            
            # 3. Process investment calculations
            investments_updated = self.update_investments()
            
            # 4. Execute scenarios if enabled
            scenarios_executed = 0
            if self.enable_scenarios:
                scenarios_executed = self.execute_scenarios()
            
            # 5. Simulate trades if enabled
            trades_simulated = 0
            if self.simulate_trades:
                trades_simulated = self.simulate_trading_activity()
            
            # 6. Cleanup old data periodically
            if self.task_counter % 100 == 0:  # Every 500 seconds (100 cycles * 5s)
                self.cleanup_old_data()
            
            # Update task completion
            duration = (timezone.now() - start_time).total_seconds()
            task.status = 'completed'
            task.completed_at = timezone.now()
            task.duration_seconds = Decimal(str(duration))
            task.items_processed = updated_count
            task.success_count = updated_count
            task.task_data = {
                'cryptos_updated': updated_count,
                'signals_generated': signals_generated,
                'investments_updated': investments_updated,
                'scenarios_executed': scenarios_executed,
                'trades_simulated': trades_simulated,
            }
            task.save()

            if self.verbose:
                self.stdout.write(
                    f"   ✅ Updated {updated_count} cryptos, "
                    f"{signals_generated} signals, "
                    f"{investments_updated} investments in {duration:.2f}s"
                )

        except Exception as e:
            task.status = 'failed'
            task.completed_at = timezone.now()
            task.error_messages = str(e)
            task.save()
            logger.exception(f"Task cycle #{self.task_counter} failed")

    def update_crypto_prices_batch(self):
        """Update a batch of cryptocurrency prices in rotation"""
        active_cryptos = Cryptocurrency.objects.filter(is_active=True).order_by('rank', 'symbol')
        total_cryptos = active_cryptos.count()
        
        if total_cryptos == 0:
            return 0

        # Calculate batch start and end indices
        start_idx = self.crypto_rotation_index
        end_idx = min(start_idx + self.batch_size, total_cryptos)
        
        # Get the batch
        crypto_batch = active_cryptos[start_idx:end_idx]
        
        updated_count = 0
        for crypto in crypto_batch:
            try:
                # Simulate realistic price movement
                self.update_crypto_price(crypto)
                updated_count += 1
            except Exception as e:
                logger.error(f"Error updating {crypto.symbol}: {str(e)}")

        # Update rotation index
        self.crypto_rotation_index = end_idx if end_idx < total_cryptos else 0
        
        # Check if we completed a full rotation
        if self.crypto_rotation_index == 0:
            self.last_full_update = timezone.now()
            if self.verbose:
                self.stdout.write(f"   🔄 Completed full rotation of {total_cryptos} cryptocurrencies")

        return updated_count

    def update_crypto_price(self, crypto):
        """Update individual cryptocurrency price with realistic movement"""
        settings = TradingSettings.objects.first()
        
        # Calculate price movement based on various factors
        base_volatility = self.calculate_base_volatility(crypto)
        market_sentiment = self.calculate_market_sentiment()
        
        # Generate price change percentage (-5% to +5% typically)
        max_change = base_volatility * (market_sentiment + 1.0)
        price_change_pct = (random.random() - 0.5) * 2 * max_change
        
        # Apply the price change
        old_price = crypto.current_price
        new_price = old_price * (1 + Decimal(str(price_change_pct / 100)))
        
        # Ensure minimum price
        if new_price < Decimal('0.000001'):
            new_price = Decimal('0.000001')
        
        # Update cryptocurrency data
        crypto.current_price = new_price
        
        # Update percentage changes (simulate realistic values)
        crypto.price_change_1h = Decimal(str(round(price_change_pct * 0.3, 4)))
        crypto.price_change_24h = Decimal(str(round(price_change_pct, 4)))
        crypto.price_change_7d = Decimal(str(round(price_change_pct * 1.5, 4)))
        crypto.price_change_30d = Decimal(str(round(price_change_pct * 3, 4)))
        
        # Update volume (simulate realistic changes)
        volume_change = (random.random() - 0.5) * 0.4  # -20% to +20%
        crypto.volume_24h = crypto.volume_24h * (1 + Decimal(str(volume_change)))
        
        # Update market cap
        crypto.market_cap = crypto.current_price * crypto.circulating_supply
        
        crypto.save()
        
        # Log price movement
        PriceMovementLog.objects.create(
            cryptocurrency=crypto,
            previous_price=old_price,
            new_price=new_price,
            price_change=new_price - old_price,
            price_change_percent=Decimal(str(price_change_pct)),
            movement_type='natural',
            volume_affected=crypto.volume_24h
        )
        
        # Store historical price data
        PriceData.objects.create(
            cryptocurrency=crypto,
            price=new_price,
            volume=crypto.volume_24h,
            market_cap=crypto.market_cap,
            timestamp=timezone.now(),
            source='automated_system'
        )

    def calculate_base_volatility(self, crypto):
        """Calculate base volatility for a cryptocurrency"""
        # Different crypto categories have different volatilities
        if crypto.is_stablecoin:
            return 0.1  # Very low volatility for stablecoins
        
        volatility_map = {
            'Store of Value': 2.0,  # BTC-like
            'Layer 1': 3.0,         # ETH, ADA, SOL
            'DeFi': 5.0,            # DeFi tokens
            'Meme': 10.0,           # Meme coins
            'Exchange Token': 3.5,   # Exchange tokens
            'Gaming': 6.0,          # Gaming tokens
            'NFT': 7.0,             # NFT tokens
            'Privacy': 4.0,         # Privacy coins
        }
        
        # Find the highest volatility category
        max_volatility = 4.0  # Default
        for category in crypto.categories:
            if category in volatility_map:
                max_volatility = max(max_volatility, volatility_map[category])
        
        return max_volatility

    def calculate_market_sentiment(self):
        """Calculate overall market sentiment (-1 to 1)"""
        # Simple sentiment based on time and randomness
        import math
        
        # Time-based sentiment (daily cycles)
        time_factor = math.sin((timezone.now().hour / 24.0) * 2 * math.pi) * 0.3
        
        # Random market events
        random_factor = (random.random() - 0.5) * 0.4
        
        sentiment = time_factor + random_factor
        return max(-1.0, min(1.0, sentiment))

    def generate_trading_signals(self):
        """Generate trading signals for cryptocurrencies"""
        # Focus on top cryptocurrencies for signals
        top_cryptos = Cryptocurrency.objects.filter(
            is_active=True, 
            rank__lte=50
        ).order_by('rank')[:10]
        
        signals_generated = 0
        
        for crypto in top_cryptos:
            try:
                # Simple signal generation based on price movements
                if crypto.price_change_24h > 5:
                    signal_type = 'sell'
                    confidence = min(95, 60 + abs(crypto.price_change_24h))
                elif crypto.price_change_24h < -5:
                    signal_type = 'buy'
                    confidence = min(95, 60 + abs(crypto.price_change_24h))
                else:
                    signal_type = 'hold'
                    confidence = 50 + random.randint(0, 20)
                
                # Create or update signal
                signal, created = TradingSignal.objects.get_or_create(
                    cryptocurrency=crypto,
                    is_active=True,
                    defaults={
                        'signal_type': signal_type,
                        'confidence': Decimal(str(confidence)),
                        'reasoning': f'Generated from 24h price change of {crypto.price_change_24h}%',
                        'indicators': {
                            'price_change_24h': float(crypto.price_change_24h),
                            'volume_24h': float(crypto.volume_24h),
                            'rsi': 50 + random.randint(-20, 20),
                            'macd': random.choice(['bullish', 'bearish', 'neutral']),
                        }
                    }
                )
                
                if not created:
                    # Update existing signal
                    signal.signal_type = signal_type
                    signal.confidence = Decimal(str(confidence))
                    signal.reasoning = f'Updated from 24h price change of {crypto.price_change_24h}%'
                    signal.indicators['price_change_24h'] = float(crypto.price_change_24h)
                    signal.save()
                
                signals_generated += 1
                
            except Exception as e:
                logger.error(f"Error generating signal for {crypto.symbol}: {str(e)}")
        
        return signals_generated

    def update_investments(self):
        """Update user investment calculations"""
        active_investments = CryptoInvestment.objects.filter(status='active')[:50]  # Limit for performance
        investments_updated = 0
        
        for investment in active_investments:
            try:
                # Update investment value based on current crypto prices
                if investment.cryptocurrency:
                    current_crypto_price = investment.cryptocurrency.current_price
                    # Simple calculation - in real system this would be more complex
                    investment.current_value_btc = investment.total_invested_btc * (
                        current_crypto_price / Decimal('50000')  # Normalized against BTC price
                    )
                    investment.unrealized_pnl_btc = investment.current_value_btc - investment.total_invested_btc
                    investment.unrealized_pnl_percent = (
                        (investment.unrealized_pnl_btc / investment.total_invested_btc) * 100 
                        if investment.total_invested_btc > 0 else 0
                    )
                    investment.save()
                    investments_updated += 1
                    
            except Exception as e:
                logger.error(f"Error updating investment {investment.id}: {str(e)}")
        
        return investments_updated

    def execute_scenarios(self):
        """Execute active profit/loss scenarios"""
        active_scenarios = ProfitLossScenario.objects.filter(
            is_active=True,
            scheduled_execution__lte=timezone.now()
        )[:5]  # Limit scenarios per cycle
        
        scenarios_executed = 0
        
        for scenario in active_scenarios:
            try:
                if scenario.target_cryptocurrency:
                    self.apply_scenario_to_crypto(scenario, scenario.target_cryptocurrency)
                elif scenario.apply_to_all_investments:
                    # Apply to top 10 cryptos
                    top_cryptos = Cryptocurrency.objects.filter(rank__lte=10)[:10]
                    for crypto in top_cryptos:
                        self.apply_scenario_to_crypto(scenario, crypto)
                
                # Update scenario execution tracking
                scenario.times_executed += 1
                scenario.last_executed = timezone.now()
                if scenario.execute_immediately:
                    scenario.is_active = False  # One-time scenario
                scenario.save()
                
                scenarios_executed += 1
                
            except Exception as e:
                logger.error(f"Error executing scenario {scenario.id}: {str(e)}")
        
        return scenarios_executed

    def apply_scenario_to_crypto(self, scenario, crypto):
        """Apply a scenario to a specific cryptocurrency"""
        old_price = crypto.current_price
        price_multiplier = 1 + (scenario.percentage_change / 100)
        new_price = old_price * Decimal(str(price_multiplier))
        
        crypto.current_price = new_price
        crypto.market_cap = new_price * crypto.circulating_supply
        crypto.save()
        
        # Log the scenario execution
        PriceMovementLog.objects.create(
            cryptocurrency=crypto,
            previous_price=old_price,
            new_price=new_price,
            price_change=new_price - old_price,
            price_change_percent=scenario.percentage_change,
            movement_type='scenario_based',
            triggered_by_scenario=scenario,
            notes=f'Scenario: {scenario.name}'
        )

    def simulate_trading_activity(self):
        """Simulate realistic trading activity"""
        if not User.objects.exists():
            return 0
        
        # Get a sample user for simulation
        user = User.objects.first()
        top_cryptos = Cryptocurrency.objects.filter(rank__lte=20)[:5]
        
        trades_created = 0
        
        for crypto in top_cryptos:
            # Random chance to create a trade
            if random.random() < 0.1:  # 10% chance per crypto
                trade_type = random.choice(['buy', 'sell'])
                amount = Decimal(str(random.uniform(0.01, 1.0)))
                
                Trade.objects.create(
                    user=user,
                    cryptocurrency=crypto,
                    trade_type=trade_type,
                    amount=amount,
                    price=crypto.current_price,
                    total_value=amount * crypto.current_price,
                    status='executed',
                    executed_at=timezone.now(),
                    notes='Simulated trade'
                )
                trades_created += 1
        
        return trades_created

    def cleanup_old_data(self):
        """Clean up old historical data to prevent database bloat"""
        cutoff_date = timezone.now() - timedelta(days=30)
        
        # Keep only recent price data
        PriceData.objects.filter(timestamp__lt=cutoff_date).delete()
        
        # Keep only recent price movement logs
        PriceMovementLog.objects.filter(timestamp__lt=cutoff_date).delete()
        
        # Keep only recent automated tasks
        AutomatedTask.objects.filter(created_at__lt=cutoff_date).delete()
        
        self.stdout.write("   🧹 Cleaned up old data")

    def get_or_create_settings(self):
        """Get or create trading settings"""
        settings, created = TradingSettings.objects.get_or_create(
            defaults={
                'trading_enabled': True,
                'maintenance_mode': False,
                'profit_loss_mode': 'automatic',
                'price_update_frequency': self.interval,
            }
        )
        return settings