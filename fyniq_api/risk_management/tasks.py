import logging
from decimal import Decimal
from celery import shared_task
from django.utils import timezone
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task
def check_risk_limits():
    """Check risk limits for all users"""
    try:
        from accounts.models import User
        from .models import RiskProfile, RiskLimit
        
        # Get all users with risk profiles
        users = User.objects.filter(risk_profiles__isnull=False).distinct()
        
        for user in users:
            try:
                # Check risk limits for this user
                check_user_risk_limits.delay(user.id)
                
            except Exception as e:
                logger.error(f"Error checking risk limits for user {user.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in check_risk_limits: {str(e)}")
        raise

@shared_task
def check_user_risk_limits(user_id):
    """Check risk limits for a specific user"""
    try:
        from accounts.models import User
        from .models import RiskProfile, RiskLimit, RiskViolation
        from portfolio_management.models import Portfolio, Position
        from order_management.models import Order
        
        user = User.objects.get(id=user_id)
        
        # Get user's risk profile
        risk_profile = RiskProfile.objects.filter(user=user).first()
        if not risk_profile:
            logger.warning(f"No risk profile found for user {user_id}")
            return False
        
        # Get user's portfolio
        portfolio = Portfolio.objects.filter(user=user).first()
        if not portfolio:
            logger.warning(f"No portfolio found for user {user_id}")
            return False
        
        # Check various risk limits
        violations = []
        
        # Check position size limits
        position_violations = check_position_size_limits(user, risk_profile)
        violations.extend(position_violations)
        
        # Check portfolio concentration limits
        concentration_violations = check_concentration_limits(user, risk_profile, portfolio)
        violations.extend(concentration_violations)
        
        # Check drawdown limits
        drawdown_violations = check_drawdown_limits(user, risk_profile, portfolio)
        violations.extend(drawdown_violations)
        
        # Check leverage limits
        leverage_violations = check_leverage_limits(user, risk_profile, portfolio)
        violations.extend(leverage_violations)
        
        # Create violation records
        for violation_data in violations:
            violation = RiskViolation.objects.create(
                user=user,
                risk_profile=risk_profile,
                violation_type=violation_data['type'],
                severity=violation_data['severity'],
                description=violation_data['description'],
                current_value=violation_data['current_value'],
                limit_value=violation_data['limit_value'],
                triggered_at=timezone.now(),
            )
            
            # Send alert
            from alerts.tasks import create_risk_alert
            create_risk_alert.delay(
                user_id=user.id,
                alert_type=violation_data['type'],
                severity=violation_data['severity'],
                message=violation_data['description']
            )
        
        if violations:
            logger.warning(f"Found {len(violations)} risk violations for user {user_id}")
        else:
            logger.info(f"No risk violations found for user {user_id}")
        
        return True
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error checking risk limits for user {user_id}: {str(e)}")
        raise

@shared_task
def calculate_var():
    """Calculate Value at Risk for all portfolios"""
    try:
        from portfolio_management.models import Portfolio
        
        # Get all portfolios
        portfolios = Portfolio.objects.all()
        
        for portfolio in portfolios:
            try:
                # Calculate VaR for this portfolio
                calculate_portfolio_var.delay(portfolio.id)
                
            except Exception as e:
                logger.error(f"Error calculating VaR for portfolio {portfolio.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in calculate_var: {str(e)}")
        raise

@shared_task
def calculate_portfolio_var(portfolio_id):
    """Calculate Value at Risk for a specific portfolio"""
    try:
        from portfolio_management.models import Portfolio, Position
        from .models import RiskMetric
        
        portfolio = Portfolio.objects.get(id=portfolio_id)
        
        # Get portfolio positions
        positions = Position.objects.filter(portfolio=portfolio)
        
        if not positions.exists():
            logger.info(f"No positions found for portfolio {portfolio_id}")
            return False
        
        # Calculate portfolio VaR (simplified calculation)
        total_value = portfolio.total_value
        var_95 = total_value * Decimal('0.05')  # 5% VaR at 95% confidence
        var_99 = total_value * Decimal('0.02')  # 2% VaR at 99% confidence
        
        # Create or update risk metric
        risk_metric, created = RiskMetric.objects.get_or_create(
            portfolio=portfolio,
            metric_type='var',
            defaults={
                'value': var_95,
                'confidence_level': Decimal('0.95'),
                'time_horizon': 1,  # 1 day
                'calculated_at': timezone.now(),
            }
        )
        
        if not created:
            risk_metric.value = var_95
            risk_metric.calculated_at = timezone.now()
            risk_metric.save()
        
        logger.info(f"Calculated VaR for portfolio {portfolio_id}: ${var_95:.2f}")
        return True
        
    except Portfolio.DoesNotExist:
        logger.error(f"Portfolio {portfolio_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error calculating VaR for portfolio {portfolio_id}: {str(e)}")
        raise

@shared_task
def monitor_market_risk():
    """Monitor market-wide risk factors"""
    try:
        from .models import MarketRiskFactor
        
        # Check for high volatility
        check_volatility_risk.delay()
        
        # Check for liquidity issues
        check_liquidity_risk.delay()
        
        # Check for correlation breakdown
        check_correlation_risk.delay()
        
        return True
        
    except Exception as e:
        logger.error(f"Error in monitor_market_risk: {str(e)}")
        raise

@shared_task
def check_volatility_risk():
    """Check for high volatility risk"""
    try:
        from market_data.models import Ticker
        
        # Get recent ticker data for major pairs
        major_pairs = ['BTC/USD', 'ETH/USD', 'BNB/USD']
        
        for pair in major_pairs:
            try:
                # Get recent ticker data
                tickers = Ticker.objects.filter(
                    trading_pair=pair,
                    timestamp__gte=timezone.now() - timezone.timedelta(hours=24)
                ).order_by('timestamp')
                
                if tickers.count() < 2:
                    continue
                
                # Calculate volatility
                prices = [t.last_price for t in tickers]
                returns = []
                for i in range(1, len(prices)):
                    returns.append((prices[i] - prices[i-1]) / prices[i-1])
                
                if returns:
                    volatility = sum(abs(r) for r in returns) / len(returns)
                    
                    # Check if volatility is high
                    if volatility > Decimal('0.05'):  # 5% average daily volatility
                        # Create market risk factor
                        from .models import MarketRiskFactor
                        risk_factor = MarketRiskFactor.objects.create(
                            factor_type='high_volatility',
                            trading_pair=pair,
                            severity='high',
                            description=f"High volatility detected for {pair}: {volatility:.2%}",
                            value=volatility,
                            threshold=Decimal('0.05'),
                            detected_at=timezone.now(),
                        )
                        
                        logger.warning(f"High volatility detected for {pair}: {volatility:.2%}")
                
            except Exception as e:
                logger.error(f"Error checking volatility for {pair}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in check_volatility_risk: {str(e)}")
        raise

@shared_task
def check_liquidity_risk():
    """Check for liquidity risk"""
    try:
        from market_data.models import OrderBook
        
        # Get recent order book data
        order_books = OrderBook.objects.filter(
            timestamp__gte=timezone.now() - timezone.timedelta(hours=1)
        )
        
        for order_book in order_books:
            try:
                # Calculate bid-ask spread
                if order_book.bids and order_book.asks:
                    best_bid = max(bid[0] for bid in order_book.bids)
                    best_ask = min(ask[0] for ask in order_book.asks)
                    spread = (best_ask - best_bid) / best_bid
                    
                    # Check if spread is wide (indicating low liquidity)
                    if spread > Decimal('0.01'):  # 1% spread
                        from .models import MarketRiskFactor
                        risk_factor = MarketRiskFactor.objects.create(
                            factor_type='low_liquidity',
                            trading_pair=order_book.trading_pair,
                            severity='medium',
                            description=f"Wide bid-ask spread for {order_book.trading_pair}: {spread:.2%}",
                            value=spread,
                            threshold=Decimal('0.01'),
                            detected_at=timezone.now(),
                        )
                        
                        logger.warning(f"Low liquidity detected for {order_book.trading_pair}: {spread:.2%} spread")
                
            except Exception as e:
                logger.error(f"Error checking liquidity for {order_book.trading_pair}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in check_liquidity_risk: {str(e)}")
        raise

@shared_task
def check_correlation_risk():
    """Check for correlation breakdown risk"""
    try:
        # This would calculate correlations between different assets
        # For now, just log that we're checking correlations
        logger.info("Checking correlation risk")
        return True
        
    except Exception as e:
        logger.error(f"Error in check_correlation_risk: {str(e)}")
        raise

def check_position_size_limits(user, risk_profile):
    """Check position size limits"""
    violations = []
    
    try:
        from portfolio_management.models import Position
        
        # Get user's positions
        positions = Position.objects.filter(user=user)
        
        for position in positions:
            # Check if position size exceeds limit
            position_value = position.amount * position.avg_entry_price
            portfolio_value = position.portfolio.total_value if position.portfolio else Decimal('0')
            
            if portfolio_value > 0:
                position_size_pct = position_value / portfolio_value
                
                if position_size_pct > risk_profile.max_position_size:
                    violations.append({
                        'type': 'position_size_limit',
                        'severity': 'high',
                        'description': f"Position size limit exceeded for {position.trading_pair}",
                        'current_value': position_size_pct,
                        'limit_value': risk_profile.max_position_size,
                    })
    
    except Exception as e:
        logger.error(f"Error checking position size limits: {str(e)}")
    
    return violations

def check_concentration_limits(user, risk_profile, portfolio):
    """Check portfolio concentration limits"""
    violations = []
    
    try:
        from portfolio_management.models import Position
        
        # Get user's positions
        positions = Position.objects.filter(user=user)
        
        # Calculate concentration by asset
        asset_concentrations = {}
        total_value = portfolio.total_value
        
        for position in positions:
            asset = position.trading_pair.split('/')[0]  # Get base currency
            position_value = position.amount * position.avg_entry_price
            
            if asset not in asset_concentrations:
                asset_concentrations[asset] = Decimal('0')
            asset_concentrations[asset] += position_value
        
        # Check concentration limits
        for asset, value in asset_concentrations.items():
            concentration_pct = value / total_value if total_value > 0 else Decimal('0')
            
            if concentration_pct > risk_profile.max_concentration:
                violations.append({
                    'type': 'concentration_limit',
                    'severity': 'medium',
                    'description': f"Concentration limit exceeded for {asset}",
                    'current_value': concentration_pct,
                    'limit_value': risk_profile.max_concentration,
                })
    
    except Exception as e:
        logger.error(f"Error checking concentration limits: {str(e)}")
    
    return violations

def check_drawdown_limits(user, risk_profile, portfolio):
    """Check drawdown limits"""
    violations = []
    
    try:
        from portfolio_management.models import PortfolioSnapshot
        
        # Get portfolio snapshots
        snapshots = PortfolioSnapshot.objects.filter(
            portfolio=portfolio
        ).order_by('-timestamp')[:30]  # Last 30 snapshots
        
        if len(snapshots) < 2:
            return violations
        
        # Calculate current drawdown
        peak_value = max(s.value for s in snapshots)
        current_value = portfolio.total_value
        drawdown = (peak_value - current_value) / peak_value if peak_value > 0 else Decimal('0')
        
        if drawdown > risk_profile.max_drawdown:
            violations.append({
                'type': 'drawdown_limit',
                'severity': 'high',
                'description': f"Drawdown limit exceeded: {drawdown:.2%}",
                'current_value': drawdown,
                'limit_value': risk_profile.max_drawdown,
            })
    
    except Exception as e:
        logger.error(f"Error checking drawdown limits: {str(e)}")
    
    return violations

def check_leverage_limits(user, risk_profile, portfolio):
    """Check leverage limits"""
    violations = []
    
    try:
        # Calculate current leverage
        # This would depend on your leverage calculation logic
        current_leverage = Decimal('1.0')  # Placeholder
        
        if current_leverage > risk_profile.max_leverage:
            violations.append({
                'type': 'leverage_limit',
                'severity': 'high',
                'description': f"Leverage limit exceeded: {current_leverage}x",
                'current_value': current_leverage,
                'limit_value': risk_profile.max_leverage,
            })
    
    except Exception as e:
        logger.error(f"Error checking leverage limits: {str(e)}")
    
    return violations 