from django.conf import settings
from decimal import Decimal

class RiskManagementService:
    def __init__(self):
        self.config = getattr(settings, 'RISK_CONFIG', {})

    def check_position_size(self, position_size):
        max_size = Decimal(self.config.get('MAX_POSITION_SIZE', 10000))
        return position_size <= max_size

    def check_leverage(self, leverage):
        max_leverage = Decimal(self.config.get('MAX_LEVERAGE', 10))
        return leverage <= max_leverage

    def check_daily_loss(self, user, daily_loss):
        max_loss = Decimal(self.config.get('MAX_DAILY_LOSS', 1000))
        return daily_loss <= max_loss

    def check_open_positions(self, user, open_positions):
        max_positions = int(self.config.get('MAX_OPEN_POSITIONS', 5))
        return open_positions <= max_positions

    def check_margin(self, margin_ratio):
        min_margin = Decimal(self.config.get('MIN_MARGIN_REQUIREMENT', 0.1))
        return margin_ratio >= min_margin

    def check_liquidation(self, margin_ratio):
        threshold = Decimal(self.config.get('LIQUIDATION_THRESHOLD', 0.05))
        return margin_ratio < threshold 