import logging
from decimal import Decimal
from celery import shared_task
from django.utils import timezone
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task
def update_portfolio_values():
    """Update portfolio values for all users"""
    try:
        from accounts.models import User
        from .models import Portfolio
        
        # Get all users with portfolios
        users = User.objects.filter(portfolios__isnull=False).distinct()
        
        for user in users:
            try:
                # Update portfolio for this user
                update_user_portfolio.delay(user.id)
                
            except Exception as e:
                logger.error(f"Error updating portfolio for user {user.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in update_portfolio_values: {str(e)}")
        raise

@shared_task
def update_user_portfolio(user_id):
    """Update portfolio for a specific user"""
    try:
        from accounts.models import User
        from .models import Portfolio, Position, Balance, PortfolioSnapshot
        from market_data.models import Ticker
        
        user = User.objects.get(id=user_id)
        
        # Get or create portfolio
        portfolio, created = Portfolio.objects.get_or_create(
            user=user,
            defaults={
                'name': f"{user.username}'s Portfolio",
                'description': 'Main trading portfolio',
                'currency': 'USD',
            }
        )
        
        # Get user's positions
        positions = Position.objects.filter(user=user)
        
        # Get user's balances
        balances = Balance.objects.filter(user=user)
        
        # Calculate total value
        total_value = Decimal('0')
        
        # Add position values
        for position in positions:
            # Get current price for position
            ticker = Ticker.objects.filter(
                trading_pair=position.trading_pair
            ).order_by('-timestamp').first()
            
            if ticker:
                current_price = ticker.last_price
                position_value = position.amount * current_price
                total_value += position_value
                
                # Update position current value
                position.current_value = position_value
                position.current_price = current_price
                position.save()
        
        # Add balance values
        for balance in balances:
            if balance.currency == portfolio.currency:
                total_value += balance.amount
            else:
                # Convert to portfolio currency (simplified)
                # In a real implementation, you'd use exchange rates
                total_value += balance.amount
        
        # Update portfolio
        portfolio.total_value = total_value
        portfolio.last_updated = timezone.now()
        portfolio.save()
        
        # Create portfolio snapshot
        snapshot = PortfolioSnapshot.objects.create(
            portfolio=portfolio,
            value=total_value,
            timestamp=timezone.now(),
        )
        
        # Calculate performance metrics
        calculate_portfolio_performance.delay(portfolio.id)
        
        logger.info(f"Updated portfolio for user {user_id}: ${total_value:.2f}")
        return True
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error updating portfolio for user {user_id}: {str(e)}")
        raise

@shared_task
def calculate_portfolio_performance(portfolio_id):
    """Calculate performance metrics for a portfolio"""
    try:
        from .models import Portfolio, PortfolioSnapshot, PortfolioPerformance
        
        portfolio = Portfolio.objects.get(id=portfolio_id)
        
        # Get portfolio snapshots
        snapshots = PortfolioSnapshot.objects.filter(
            portfolio=portfolio
        ).order_by('timestamp')
        
        if snapshots.count() < 2:
            logger.info(f"Not enough snapshots for portfolio {portfolio_id}")
            return False
        
        # Calculate performance metrics
        first_snapshot = snapshots.first()
        last_snapshot = snapshots.last()
        
        # Calculate total return
        total_return = (last_snapshot.value - first_snapshot.value) / first_snapshot.value if first_snapshot.value > 0 else Decimal('0')
        
        # Calculate daily returns
        daily_returns = []
        for i in range(1, snapshots.count()):
            prev_value = snapshots[i-1].value
            curr_value = snapshots[i].value
            if prev_value > 0:
                daily_return = (curr_value - prev_value) / prev_value
                daily_returns.append(daily_return)
        
        # Calculate metrics
        if daily_returns:
            avg_daily_return = sum(daily_returns) / len(daily_returns)
            
            # Calculate volatility (standard deviation)
            variance = sum((r - avg_daily_return) ** 2 for r in daily_returns) / len(daily_returns)
            volatility = variance.sqrt()
            
            # Calculate Sharpe ratio (simplified, assuming 0% risk-free rate)
            sharpe_ratio = avg_daily_return / volatility if volatility > 0 else Decimal('0')
            
            # Calculate max drawdown
            peak_value = first_snapshot.value
            max_drawdown = Decimal('0')
            
            for snapshot in snapshots:
                if snapshot.value > peak_value:
                    peak_value = snapshot.value
                else:
                    drawdown = (peak_value - snapshot.value) / peak_value if peak_value > 0 else Decimal('0')
                    max_drawdown = max(max_drawdown, drawdown)
        else:
            avg_daily_return = Decimal('0')
            volatility = Decimal('0')
            sharpe_ratio = Decimal('0')
            max_drawdown = Decimal('0')
        
        # Create or update performance record
        performance, created = PortfolioPerformance.objects.get_or_create(
            portfolio=portfolio,
            period='daily',
            defaults={
                'total_return': total_return,
                'avg_daily_return': avg_daily_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'calculated_at': timezone.now(),
            }
        )
        
        if not created:
            performance.total_return = total_return
            performance.avg_daily_return = avg_daily_return
            performance.volatility = volatility
            performance.sharpe_ratio = sharpe_ratio
            performance.max_drawdown = max_drawdown
            performance.calculated_at = timezone.now()
            performance.save()
        
        logger.info(f"Calculated performance for portfolio {portfolio_id}")
        return True
        
    except Portfolio.DoesNotExist:
        logger.error(f"Portfolio {portfolio_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error calculating performance for portfolio {portfolio_id}: {str(e)}")
        raise

@shared_task
def update_asset_allocation(portfolio_id):
    """Update asset allocation for a portfolio"""
    try:
        from .models import Portfolio, Position, AssetAllocation
        from market_data.models import Ticker
        
        portfolio = Portfolio.objects.get(id=portfolio_id)
        
        # Get portfolio positions
        positions = Position.objects.filter(user=portfolio.user)
        
        if not positions.exists():
            logger.info(f"No positions found for portfolio {portfolio_id}")
            return False
        
        # Calculate asset allocation
        total_value = portfolio.total_value
        allocations = {}
        
        for position in positions:
            # Get current price
            ticker = Ticker.objects.filter(
                trading_pair=position.trading_pair
            ).order_by('-timestamp').first()
            
            if ticker:
                position_value = position.amount * ticker.last_price
                asset = position.trading_pair.split('/')[0]  # Get base currency
                
                if asset not in allocations:
                    allocations[asset] = Decimal('0')
                allocations[asset] += position_value
        
        # Create or update allocation records
        for asset, value in allocations.items():
            allocation_pct = value / total_value if total_value > 0 else Decimal('0')
            
            allocation, created = AssetAllocation.objects.get_or_create(
                portfolio=portfolio,
                asset=asset,
                defaults={
                    'allocation_percentage': allocation_pct,
                    'value': value,
                    'last_updated': timezone.now(),
                }
            )
            
            if not created:
                allocation.allocation_percentage = allocation_pct
                allocation.value = value
                allocation.last_updated = timezone.now()
                allocation.save()
        
        logger.info(f"Updated asset allocation for portfolio {portfolio_id}")
        return True
        
    except Portfolio.DoesNotExist:
        logger.error(f"Portfolio {portfolio_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error updating asset allocation for portfolio {portfolio_id}: {str(e)}")
        raise

@shared_task
def rebalance_portfolio(portfolio_id):
    """Rebalance portfolio according to target allocation"""
    try:
        from .models import Portfolio, AssetAllocation
        from order_management.models import Order
        
        portfolio = Portfolio.objects.get(id=portfolio_id)
        
        # Get current and target allocations
        current_allocations = AssetAllocation.objects.filter(portfolio=portfolio)
        
        if not current_allocations.exists():
            logger.info(f"No allocations found for portfolio {portfolio_id}")
            return False
        
        # For now, just log that rebalancing would happen
        # In a real implementation, this would:
        # 1. Compare current vs target allocations
        # 2. Calculate required trades
        # 3. Create orders to rebalance
        
        logger.info(f"Portfolio rebalancing triggered for portfolio {portfolio_id}")
        return True
        
    except Portfolio.DoesNotExist:
        logger.error(f"Portfolio {portfolio_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error rebalancing portfolio {portfolio_id}: {str(e)}")
        raise

@shared_task
def generate_portfolio_report(portfolio_id, report_type='summary'):
    """Generate portfolio report"""
    try:
        from .models import Portfolio, PortfolioReport
        
        portfolio = Portfolio.objects.get(id=portfolio_id)
        
        # Generate report content
        report_content = generate_report_content(portfolio, report_type)
        
        # Create report record
        report = PortfolioReport.objects.create(
            portfolio=portfolio,
            report_type=report_type,
            title=f"{report_type.title()} Report - {timezone.now().strftime('%Y-%m-%d')}",
            content=report_content,
            generated_at=timezone.now(),
        )
        
        logger.info(f"Generated {report_type} report for portfolio {portfolio_id}")
        return report.id
        
    except Portfolio.DoesNotExist:
        logger.error(f"Portfolio {portfolio_id} not found")
        return None
    except Exception as e:
        logger.error(f"Error generating report for portfolio {portfolio_id}: {str(e)}")
        raise

def generate_report_content(portfolio, report_type):
    """Generate report content"""
    if report_type == 'summary':
        return f"""
        Portfolio Summary Report
        Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Portfolio: {portfolio.name}
        Total Value: ${portfolio.total_value:.2f}
        Currency: {portfolio.currency}
        Last Updated: {portfolio.last_updated}
        
        This is a summary report for the portfolio.
        """
    else:
        return f"Report content for {report_type} report"

@shared_task
def cleanup_old_data():
    """Clean up old portfolio data"""
    try:
        from .models import PortfolioSnapshot, PortfolioPerformance, AssetAllocation
        
        # Keep data for different periods
        cutoff_snapshots = timezone.now() - timezone.timedelta(days=90)
        cutoff_performance = timezone.now() - timezone.timedelta(days=365)
        cutoff_allocations = timezone.now() - timezone.timedelta(days=30)
        
        # Delete old records
        deleted_snapshots = PortfolioSnapshot.objects.filter(timestamp__lt=cutoff_snapshots).delete()
        deleted_performance = PortfolioPerformance.objects.filter(calculated_at__lt=cutoff_performance).delete()
        deleted_allocations = AssetAllocation.objects.filter(last_updated__lt=cutoff_allocations).delete()
        
        logger.info(f"Cleaned up old portfolio data: {deleted_snapshots[0]} snapshots, {deleted_performance[0]} performance records, {deleted_allocations[0]} allocations")
        
        return True
        
    except Exception as e:
        logger.error(f"Error cleaning up old portfolio data: {str(e)}")
        raise 