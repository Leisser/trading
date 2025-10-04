import time
import logging
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
import random

from trades.models import (
    TradingSettings, ProfitLossScenario, Cryptocurrency, CryptoIndex,
    CryptoInvestment, PriceMovementLog, AutomatedTask, UserDepositRequest
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run continuous trading tasks and financial updates'
    
    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=1, help='Update interval in seconds')
        parser.add_argument('--run-once', action='store_true', help='Run tasks once and exit')
    
    def handle(self, *args, **options):
        interval = options['interval']
        run_once = options['run_once']
        
        logger.info(f"Starting trading tasks with {interval}s interval...")
        
        if run_once:
            self.run_all_tasks()
        else:
            self.run_continuous_tasks(interval)
    
    def run_continuous_tasks(self, interval):
        """Run tasks continuously"""
        try:
            while True:
                self.run_all_tasks()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
    
    def run_all_tasks(self):
        """Run all tasks once"""
        settings = TradingSettings.objects.first()
        if not settings:
            settings = TradingSettings.objects.create()
            
        if settings.trading_enabled and not settings.maintenance_mode:
            self.update_prices(settings)
            self.update_investments()
            self.check_scenarios()
            self.check_deposits()
    
    def update_prices(self, settings):
        """Update prices based on admin settings"""
        task = AutomatedTask.objects.create(
            task_type='price_update',
            task_name='Price Update',
            status='running',
            started_at=timezone.now()
        )
        
        try:
            success_count = 0
            
            # Update cryptocurrencies
            for crypto in Cryptocurrency.objects.filter(is_active=True):
                if settings.profit_loss_mode == 'simulated':
                    change_percent = self.simulate_price_change(settings)
                    if abs(change_percent) > 0.01:
                        self.apply_crypto_change(crypto, change_percent)
                        success_count += 1
                        
            # Update indices
            for index in CryptoIndex.objects.filter(is_active=True):
                change_percent = self.simulate_index_change(settings)
                if abs(change_percent) > 0.001:
                    self.apply_index_change(index, change_percent)
                    success_count += 1
            
            # Complete task
            task.status = 'completed'
            task.completed_at = timezone.now()
            task.success_count = success_count
            task.save()
            
        except Exception as e:
            task.status = 'failed'
            task.error_messages = str(e)
            task.save()
            logger.error(f"Price update failed: {e}")
    
    def simulate_price_change(self, settings):
        """Generate realistic price changes"""
        max_change_per_second = float(settings.max_profit_rate) / 3600  # Convert hourly to per-second
        min_change_per_second = -float(settings.max_loss_rate) / 3600
        
        # Weighted random for realistic movements
        weights = [0.5, 0.3, 0.15, 0.05]
        ranges = [(-0.1, 0.1), (-0.5, 0.5), (-2.0, 2.0), (min_change_per_second, max_change_per_second)]
        
        selected_range = random.choices(ranges, weights=weights)[0]
        return random.uniform(selected_range[0], selected_range[1])
    
    def simulate_index_change(self, settings):
        """Generate index price changes"""
        base_change = self.simulate_price_change(settings)
        volatility = float(settings.index_volatility_factor)
        return base_change * volatility
    
    def apply_crypto_change(self, crypto, change_percent):
        """Apply price change to cryptocurrency"""
        old_price = crypto.current_price
        new_price = old_price * (1 + Decimal(str(change_percent / 100)))
        
        crypto.current_price = new_price
        crypto.price_change_24h = change_percent
        crypto.save()
        
        # Log movement
        PriceMovementLog.objects.create(
            cryptocurrency=crypto,
            previous_price=old_price,
            new_price=new_price,
            price_change=new_price - old_price,
            price_change_percent=Decimal(str(change_percent)),
            movement_type='natural',
            notes=f'Automated price update: {change_percent:.4f}%'
        )
        
        # Update related investments
        self.update_crypto_investments(crypto, change_percent)
    
    def apply_index_change(self, index, change_percent):
        """Apply price change to index"""
        old_value = index.current_value
        new_value = old_value * (1 + Decimal(str(change_percent / 100)))
        
        index.current_value = new_value
        index.price_change_24h = change_percent
        index.save()
        
        # Log movement
        PriceMovementLog.objects.create(
            crypto_index=index,
            previous_price=old_value,
            new_price=new_value,
            price_change=new_value - old_value,
            price_change_percent=Decimal(str(change_percent)),
            movement_type='natural',
            notes=f'Automated index update: {change_percent:.4f}%'
        )
        
        # Update related investments
        self.update_index_investments(index, change_percent)
    
    def update_crypto_investments(self, crypto, change_percent):
        """Update investments for a cryptocurrency"""
        investments = CryptoInvestment.objects.filter(
            cryptocurrency=crypto,
            status='active'
        )
        
        multiplier = Decimal(str(1 + change_percent / 100))
        
        for investment in investments:
            investment.current_value_btc *= multiplier
            investment.current_value_usd *= multiplier
            
            # Recalculate P&L
            investment.unrealized_pnl_btc = investment.current_value_btc - investment.total_invested_btc
            investment.unrealized_pnl_usd = investment.current_value_usd - investment.total_invested_usd
            
            if investment.total_invested_btc > 0:
                investment.unrealized_pnl_percent = (
                    investment.unrealized_pnl_btc / investment.total_invested_btc
                ) * 100
            
            # Update ATH and drawdown
            if investment.current_value_btc > investment.all_time_high_value:
                investment.all_time_high_value = investment.current_value_btc
            
            if investment.all_time_high_value > 0:
                drawdown = (
                    (investment.all_time_high_value - investment.current_value_btc) / 
                    investment.all_time_high_value
                ) * 100
                if drawdown > investment.max_drawdown_percent:
                    investment.max_drawdown_percent = drawdown
            
            investment.save()
    
    def update_index_investments(self, index, change_percent):
        """Update investments for an index"""
        investments = CryptoInvestment.objects.filter(
            crypto_index=index,
            status='active'
        )
        
        multiplier = Decimal(str(1 + change_percent / 100))
        
        for investment in investments:
            investment.current_value_btc *= multiplier
            investment.current_value_usd *= multiplier
            
            # Recalculate P&L
            investment.unrealized_pnl_btc = investment.current_value_btc - investment.total_invested_btc
            investment.unrealized_pnl_usd = investment.current_value_usd - investment.total_invested_usd
            
            if investment.total_invested_btc > 0:
                investment.unrealized_pnl_percent = (
                    investment.unrealized_pnl_btc / investment.total_invested_btc
                ) * 100
            
            # Update ATH and drawdown
            if investment.current_value_btc > investment.all_time_high_value:
                investment.all_time_high_value = investment.current_value_btc
            
            if investment.all_time_high_value > 0:
                drawdown = (
                    (investment.all_time_high_value - investment.current_value_btc) / 
                    investment.all_time_high_value
                ) * 100
                if drawdown > investment.max_drawdown_percent:
                    investment.max_drawdown_percent = drawdown
            
            investment.save()
    
    def update_investments(self):
        """Update investment calculations"""
        task = AutomatedTask.objects.create(
            task_type='investment_calculation',
            task_name='Investment Updates',
            status='running',
            started_at=timezone.now()
        )
        
        try:
            # This is handled in price updates
            task.status = 'completed'
            task.completed_at = timezone.now()
            task.save()
        except Exception as e:
            task.status = 'failed'
            task.error_messages = str(e)
            task.save()
    
    def check_scenarios(self):
        """Check and execute scheduled scenarios"""
        scenarios = ProfitLossScenario.objects.filter(
            is_active=True,
            execute_immediately=True
        )
        
        for scenario in scenarios:
            try:
                self.execute_scenario(scenario)
                scenario.times_executed += 1
                scenario.last_executed = timezone.now()
                scenario.execute_immediately = False
                scenario.save()
            except Exception as e:
                logger.error(f"Scenario execution failed: {e}")
    
    def execute_scenario(self, scenario):
        """Execute a profit/loss scenario"""
        change_percent = float(scenario.percentage_change)
        
        if scenario.target_cryptocurrency:
            self.apply_crypto_change(scenario.target_cryptocurrency, change_percent)
        elif scenario.target_crypto_index:
            self.apply_index_change(scenario.target_crypto_index, change_percent)
        elif scenario.apply_to_all_investments:
            for crypto in Cryptocurrency.objects.filter(is_active=True):
                self.apply_crypto_change(crypto, change_percent)
            for index in CryptoIndex.objects.filter(is_active=True):
                self.apply_index_change(index, change_percent)
    
    def check_deposits(self):
        """Check deposit statuses"""
        # Mark expired deposits
        UserDepositRequest.objects.filter(
            status='pending',
            expires_at__lte=timezone.now()
        ).update(status='expired')