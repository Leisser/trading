"""
Portfolio Management Services
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
                'total_value': total_value,
                'total_pnl': total_pnl,
                'total_pnl_percentage': total_pnl_percentage,
                'total_transactions': total_transactions,
                'total_deposits': total_deposits,
                'total_withdrawals': total_withdrawals,
                'asset_count': balances.count()
            }
            
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            return {}
    
    @staticmethod
    def rebalance_portfolio(portfolio: Portfolio, target_allocations: Dict[str, Decimal]) -> bool:
        """Rebalance portfolio to target allocations"""
        try:
            # Get current balances
            balances = PortfolioBalance.objects.filter(portfolio=portfolio)
            total_value = sum(balance.current_value for balance in balances)
            
            if total_value == 0:
                return False
            
            # Calculate rebalancing transactions
            for balance in balances:
                target_percentage = target_allocations.get(balance.symbol, Decimal('0'))
                target_value = total_value * (target_percentage / 100)
                current_value = balance.current_value
                
                difference = target_value - current_value
                
                if abs(difference) > Decimal('0.01'):  # Minimum threshold
                    # Create rebalancing transaction
                    Transaction.objects.create(
                        portfolio=portfolio,
                        transaction_type='transfer',
                        symbol=balance.symbol,
                        amount=abs(difference),
                        value=abs(difference),
                        notes=f'Rebalancing to {target_percentage}% allocation'
                    )
            
            return True
            
        except Exception as e:
            logger.error(f"Error rebalancing portfolio: {e}")
            return False


class PnLService:
    """Service for profit and loss calculations"""
    
    @staticmethod
    def calculate_daily_pnl(portfolio: Portfolio, date: datetime.date) -> Dict:
        """Calculate daily P&L for a portfolio"""
        try:
            # Get previous day's P&L record
            previous_pnl = PnLRecord.objects.filter(
                portfolio=portfolio,
                date__lt=date
            ).order_by('-date').first()
            
            # Get current balances
            balances = PortfolioBalance.objects.filter(portfolio=portfolio)
            current_value = sum(balance.current_value for balance in balances)
            
            # Calculate P&L
            if previous_pnl:
                daily_pnl = current_value - (previous_pnl.total_pnl + current_value)
                daily_return = (daily_pnl / (current_value - daily_pnl) * 100) if current_value > daily_pnl else 0
            else:
                daily_pnl = Decimal('0')
                daily_return = Decimal('0')
            
            # Create or update P&L record
            pnl_record, created = PnLRecord.objects.get_or_create(
                portfolio=portfolio,
                date=date,
                defaults={
                    'total_pnl': daily_pnl,
                    'daily_return': daily_return,
                    'unrealized_pnl': daily_pnl,
                    'realized_pnl': Decimal('0')
                }
            )
            
            if not created:
                pnl_record.total_pnl = daily_pnl
                pnl_record.daily_return = daily_return
                pnl_record.save()
            
            return {
                'date': date,
                'daily_pnl': daily_pnl,
                'daily_return': daily_return,
                'total_value': current_value
            }
            
        except Exception as e:
            logger.error(f"Error calculating daily P&L: {e}")
            return {}
    
    @staticmethod
    def get_performance_analytics(portfolio: Portfolio, period_days: int = 30) -> Dict:
        """Get performance analytics for a portfolio"""
        try:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=period_days)
            
            # Get P&L records for the period
            pnl_records = PnLRecord.objects.filter(
                portfolio=portfolio,
                date__range=[start_date, end_date]
            ).order_by('date')
            
            if not pnl_records.exists():
                return {}
            
            # Calculate metrics
            total_return = sum(record.daily_return for record in pnl_records)
            annualized_return = (total_return / period_days) * 365
            
            # Calculate volatility (standard deviation of daily returns)
            returns = [record.daily_return for record in pnl_records]
            if len(returns) > 1:
                mean_return = sum(returns) / len(returns)
                variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
                volatility = variance ** 0.5
            else:
                volatility = Decimal('0')
            
            # Calculate Sharpe ratio (assuming risk-free rate of 2%)
            risk_free_rate = Decimal('2.0')
            sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else Decimal('0')
            
            # Calculate maximum drawdown
            max_drawdown = max(record.max_drawdown for record in pnl_records) if pnl_records.exists() else Decimal('0')
            
            # Calculate win rate
            winning_days = sum(1 for record in pnl_records if record.daily_return > 0)
            win_rate = (winning_days / len(pnl_records) * 100) if pnl_records.exists() else Decimal('0')
            
            return {
                'period_days': period_days,
                'total_return': total_return,
                'annualized_return': annualized_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'win_rate': win_rate
            }
            
        except Exception as e:
            logger.error(f"Error getting performance analytics: {e}")
            return {}


class RiskAnalyticsService:
    """Service for risk analytics and metrics"""
    
    @staticmethod
    def calculate_risk_metrics(portfolio: Portfolio) -> Dict:
        """Calculate risk metrics for a portfolio"""
        try:
            # Get recent P&L records
            pnl_records = PnLRecord.objects.filter(portfolio=portfolio).order_by('-date')[:30]
            
            if not pnl_records.exists():
                return {}
            
            # Calculate Value at Risk (VaR) - 95% confidence
            returns = [record.daily_return for record in pnl_records]
            returns.sort()
            var_95 = returns[int(len(returns) * 0.05)] if len(returns) > 20 else Decimal('0')
            
            # Calculate Expected Shortfall (CVaR)
            tail_returns = [r for r in returns if r <= var_95]
            expected_shortfall = sum(tail_returns) / len(tail_returns) if tail_returns else Decimal('0')
            
            # Calculate Beta (simplified - would need market data in real implementation)
            beta = Decimal('1.0')  # Placeholder
            
            # Calculate correlation matrix (simplified)
            correlation_matrix = {
                'BTC': {'ETH': 0.7, 'USD': -0.1},
                'ETH': {'BTC': 0.7, 'USD': -0.1},
                'USD': {'BTC': -0.1, 'ETH': -0.1}
            }
            
            # Calculate diversification ratio
            balances = PortfolioBalance.objects.filter(portfolio=portfolio)
            if balances.count() > 1:
                diversification_ratio = Decimal('1.2')  # Placeholder
            else:
                diversification_ratio = Decimal('1.0')
            
            return {
                'value_at_risk': var_95,
                'expected_shortfall': expected_shortfall,
                'beta': beta,
                'correlation_matrix': correlation_matrix,
                'diversification_ratio': diversification_ratio
            }
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics: {e}")
            return {}
