"""
Portfolio Management Services for balance tracking, P&L, and analytics.
"""
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum, Avg, Count, Q, F
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

from .models import Portfolio, PortfolioBalance, Transaction, PnLRecord, AssetAllocation

logger = logging.getLogger(__name__)

class PortfolioService:
    """Service for portfolio management operations"""
    
    @staticmethod
    def get_portfolio_summary(portfolio: Portfolio, currency: str = 'USD') -> Dict:
        """Get comprehensive portfolio summary"""
        try:
            # Get current balances
            balances = PortfolioBalance.objects.filter(portfolio=portfolio)
            total_value = sum(balance.current_value for balance in balances)
            
            # Get P&L records
            pnl_records = PnLRecord.objects.filter(portfolio=portfolio).order_by('-date')
            latest_pnl = pnl_records.first() if pnl_records.exists() else None
            
            # Calculate performance metrics
            total_pnl = sum(record.total_pnl for record in pnl_records)
            total_pnl_percentage = (total_pnl / (total_value - total_pnl) * 100) if total_value > total_pnl else 0
            
            # Get transaction statistics
            transactions = Transaction.objects.filter(portfolio=portfolio)
            total_transactions = transactions.count()
            total_deposits = transactions.filter(transaction_type='deposit').aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0')
            total_withdrawals = transactions.filter(transaction_type='withdrawal').aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0')
            
            return {
                'portfolio_id': portfolio.id,
                'portfolio_name': portfolio.name,
                'total_value': total_value,
                'total_pnl': total_pnl,
                'total_pnl_percentage': total_pnl_percentage,
                'currency': currency,
                'total_assets': balances.count(),
                'total_transactions': total_transactions,
                'total_deposits': total_deposits,
                'total_withdrawals': total_withdrawals,
                'net_deposits': total_deposits - total_withdrawals,
                'last_updated': timezone.now()
            }
            
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {str(e)}")
            return {}
    
    @staticmethod
    def get_portfolio_balances(portfolio: Portfolio, asset: str = None) -> List[Dict]:
        """Get portfolio balances"""
        try:
            balances = PortfolioBalance.objects.filter(portfolio=portfolio)
            
            if asset:
                balances = balances.filter(asset=asset)
            
            balance_data = []
            for balance in balances:
                balance_data.append({
                    'asset': balance.asset,
                    'quantity': balance.quantity,
                    'current_price': balance.current_price,
                    'current_value': balance.current_value,
                    'average_cost': balance.average_cost,
                    'unrealized_pnl': balance.current_value - (balance.quantity * balance.average_cost),
                    'unrealized_pnl_percentage': (
                        (balance.current_value - (balance.quantity * balance.average_cost)) / 
                        (balance.quantity * balance.average_cost) * 100
                    ) if balance.quantity > 0 and balance.average_cost > 0 else 0,
                    'last_updated': balance.last_updated
                })
            
            return balance_data
            
        except Exception as e:
            logger.error(f"Error getting portfolio balances: {str(e)}")
            return []
    
    @staticmethod
    def get_asset_allocation(portfolio: Portfolio, currency: str = 'USD') -> List[Dict]:
        """Get asset allocation breakdown"""
        try:
            balances = PortfolioBalance.objects.filter(portfolio=portfolio)
            total_value = sum(balance.current_value for balance in balances)
            
            allocation = []
            for balance in balances:
                percentage = (balance.current_value / total_value * 100) if total_value > 0 else 0
                allocation.append({
                    'asset': balance.asset,
                    'value': balance.current_value,
                    'percentage': percentage,
                    'quantity': balance.quantity,
                    'current_price': balance.current_price
                })
            
            # Sort by percentage descending
            allocation.sort(key=lambda x: x['percentage'], reverse=True)
            
            return allocation
            
        except Exception as e:
            logger.error(f"Error getting asset allocation: {str(e)}")
            return []
    
    @staticmethod
    def get_portfolio_history(portfolio: Portfolio, period: str = '30d') -> List[Dict]:
        """Get portfolio value history"""
        try:
            # Calculate date range
            end_date = timezone.now()
            if period == '7d':
                start_date = end_date - timedelta(days=7)
            elif period == '30d':
                start_date = end_date - timedelta(days=30)
            elif period == '90d':
                start_date = end_date - timedelta(days=90)
            elif period == '1y':
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=30)
            
            # Get P&L records in date range
            pnl_records = PnLRecord.objects.filter(
                portfolio=portfolio,
                date__range=[start_date, end_date]
            ).order_by('date')
            
            history = []
            for record in pnl_records:
                history.append({
                    'date': record.date,
                    'total_value': record.total_value,
                    'total_pnl': record.total_pnl,
                    'daily_pnl': record.daily_pnl,
                    'pnl_percentage': record.pnl_percentage
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting portfolio history: {str(e)}")
            return []
    
    @staticmethod
    def rebalance_portfolio(portfolio: Portfolio, target_allocation: Dict) -> Dict:
        """Rebalance portfolio to target allocation"""
        try:
            current_allocation = PortfolioService.get_asset_allocation(portfolio)
            total_value = sum(item['value'] for item in current_allocation)
            
            rebalance_orders = []
            
            for asset, target_percentage in target_allocation.items():
                target_value = total_value * (target_percentage / 100)
                
                # Find current allocation for this asset
                current_item = next((item for item in current_allocation if item['asset'] == asset), None)
                current_value = current_item['value'] if current_item else 0
                
                difference = target_value - current_value
                
                if abs(difference) > total_value * 0.01:  # Only rebalance if difference > 1%
                    if difference > 0:
                        # Need to buy more of this asset
                        rebalance_orders.append({
                            'asset': asset,
                            'action': 'buy',
                            'amount': difference,
                            'percentage': target_percentage
                        })
                    else:
                        # Need to sell some of this asset
                        rebalance_orders.append({
                            'asset': asset,
                            'action': 'sell',
                            'amount': abs(difference),
                            'percentage': target_percentage
                        })
            
            return {
                'current_allocation': current_allocation,
                'target_allocation': target_allocation,
                'rebalance_orders': rebalance_orders,
                'total_orders': len(rebalance_orders)
            }
            
        except Exception as e:
            logger.error(f"Error rebalancing portfolio: {str(e)}")
            return {'error': str(e)}

class PnLService:
    """Service for P&L calculations and analytics"""
    
    @staticmethod
    def get_pnl_analytics(portfolio: Portfolio, period: str = '30d', currency: str = 'USD') -> Dict:
        """Get P&L analytics for a period"""
        try:
            # Calculate date range
            end_date = timezone.now()
            if period == '1d':
                start_date = end_date - timedelta(days=1)
            elif period == '7d':
                start_date = end_date - timedelta(days=7)
            elif period == '30d':
                start_date = end_date - timedelta(days=30)
            elif period == '90d':
                start_date = end_date - timedelta(days=90)
            elif period == '1y':
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=30)
            
            # Get P&L records
            pnl_records = PnLRecord.objects.filter(
                portfolio=portfolio,
                date__range=[start_date, end_date]
            ).order_by('date')
            
            if not pnl_records.exists():
                return {
                    'period': period,
                    'total_pnl': 0,
                    'total_pnl_percentage': 0,
                    'daily_pnl_avg': 0,
                    'best_day': None,
                    'worst_day': None,
                    'volatility': 0,
                    'sharpe_ratio': 0
                }
            
            # Calculate metrics
            total_pnl = sum(record.daily_pnl for record in pnl_records)
            daily_pnls = [record.daily_pnl for record in pnl_records]
            daily_pnl_avg = sum(daily_pnls) / len(daily_pnls) if daily_pnls else 0
            
            # Find best and worst days
            best_record = max(pnl_records, key=lambda x: x.daily_pnl)
            worst_record = min(pnl_records, key=lambda x: x.daily_pnl)
            
            # Calculate volatility (standard deviation of daily returns)
            if len(daily_pnls) > 1:
                mean_return = daily_pnl_avg
                variance = sum((x - mean_return) ** 2 for x in daily_pnls) / (len(daily_pnls) - 1)
                volatility = variance ** 0.5
            else:
                volatility = 0
            
            # Calculate Sharpe ratio (simplified)
            risk_free_rate = 0.02  # 2% annual risk-free rate
            sharpe_ratio = (daily_pnl_avg - risk_free_rate / 365) / volatility if volatility > 0 else 0
            
            return {
                'period': period,
                'total_pnl': total_pnl,
                'total_pnl_percentage': (total_pnl / (pnl_records.first().total_value - total_pnl) * 100) if pnl_records.first() and pnl_records.first().total_value > total_pnl else 0,
                'daily_pnl_avg': daily_pnl_avg,
                'best_day': {
                    'date': best_record.date,
                    'pnl': best_record.daily_pnl
                },
                'worst_day': {
                    'date': worst_record.date,
                    'pnl': worst_record.daily_pnl
                },
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'total_days': len(pnl_records)
            }
            
        except Exception as e:
            logger.error(f"Error getting P&L analytics: {str(e)}")
            return {}
    
    @staticmethod
    def get_performance_comparison(portfolio: Portfolio, benchmark: str = 'BTC', period: str = '30d') -> Dict:
        """Compare portfolio performance against benchmark"""
        try:
            # Get portfolio performance
            portfolio_analytics = PnLService.get_pnl_analytics(portfolio, period)
            portfolio_return = portfolio_analytics.get('total_pnl_percentage', 0)
            
            # Simulate benchmark performance (in real implementation, fetch from market data)
            benchmark_returns = {
                'BTC': {'30d': 15.5, '90d': 45.2, '1y': 120.8},
                'ETH': {'30d': 12.3, '90d': 38.7, '1y': 95.4},
                'SP500': {'30d': 2.1, '90d': 8.5, '1y': 18.2},
                'NASDAQ': {'30d': 1.8, '90d': 12.3, '1y': 22.1}
            }
            
            benchmark_return = benchmark_returns.get(benchmark, {}).get(period, 0)
            
            # Calculate outperformance
            outperformance = portfolio_return - benchmark_return
            
            return {
                'portfolio_return': portfolio_return,
                'benchmark_return': benchmark_return,
                'benchmark': benchmark,
                'period': period,
                'outperformance': outperformance,
                'outperformance_percentage': outperformance,
                'comparison': 'outperformed' if outperformance > 0 else 'underperformed' if outperformance < 0 else 'matched'
            }
            
        except Exception as e:
            logger.error(f"Error getting performance comparison: {str(e)}")
            return {}

class RiskAnalyticsService:
    """Service for risk analytics and metrics"""
    
    @staticmethod
    def get_risk_metrics(portfolio: Portfolio, period: str = '30d') -> Dict:
        """Get risk metrics for portfolio"""
        try:
            # Calculate date range
            end_date = timezone.now()
            if period == '7d':
                start_date = end_date - timedelta(days=7)
            elif period == '30d':
                start_date = end_date - timedelta(days=30)
            elif period == '90d':
                start_date = end_date - timedelta(days=90)
            elif period == '1y':
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=30)
            
            # Get P&L records
            pnl_records = PnLRecord.objects.filter(
                portfolio=portfolio,
                date__range=[start_date, end_date]
            ).order_by('date')
            
            if not pnl_records.exists():
                return {
                    'period': period,
                    'value_at_risk_95': 0,
                    'value_at_risk_99': 0,
                    'max_drawdown': 0,
                    'volatility': 0,
                    'beta': 1.0,
                    'sharpe_ratio': 0
                }
            
            # Calculate risk metrics
            daily_returns = []
            values = [record.total_value for record in pnl_records]
            
            for i in range(1, len(values)):
                daily_return = (values[i] - values[i-1]) / values[i-1]
                daily_returns.append(float(daily_return))
            
            if not daily_returns:
                return {
                    'period': period,
                    'value_at_risk_95': 0,
                    'value_at_risk_99': 0,
                    'max_drawdown': 0,
                    'volatility': 0,
                    'beta': 1.0,
                    'sharpe_ratio': 0
                }
            
            # Value at Risk (VaR) calculation
            sorted_returns = sorted(daily_returns)
            var_95_index = int(len(sorted_returns) * 0.05)
            var_99_index = int(len(sorted_returns) * 0.01)
            
            var_95 = sorted_returns[var_95_index] if var_95_index < len(sorted_returns) else 0
            var_99 = sorted_returns[var_99_index] if var_99_index < len(sorted_returns) else 0
            
            # Maximum Drawdown
            max_value = values[0]
            max_drawdown = 0
            for value in values:
                if value > max_value:
                    max_value = value
                drawdown = (max_value - value) / max_value
                max_drawdown = max(max_drawdown, drawdown)
            
            # Volatility (standard deviation)
            mean_return = sum(daily_returns) / len(daily_returns)
            variance = sum((x - mean_return) ** 2 for x in daily_returns) / len(daily_returns)
            volatility = variance ** 0.5
            
            # Sharpe Ratio
            risk_free_rate = 0.02  # 2% annual
            sharpe_ratio = (mean_return * 365 - risk_free_rate) / (volatility * (365 ** 0.5)) if volatility > 0 else 0
            
            return {
                'period': period,
                'value_at_risk_95': var_95,
                'value_at_risk_99': var_99,
                'max_drawdown': max_drawdown,
                'volatility': volatility,
                'beta': 1.0,  # Simplified, would need market data for actual calculation
                'sharpe_ratio': sharpe_ratio,
                'total_observations': len(daily_returns)
            }
            
        except Exception as e:
            logger.error(f"Error getting risk metrics: {str(e)}")
            return {}
