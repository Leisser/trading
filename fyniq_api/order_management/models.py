from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

class Order(models.Model):
    """Model for trading orders"""
    
    ORDER_TYPES = [
        ('market', 'Market'),
        ('limit', 'Limit'),
        ('stop_market', 'Stop Market'),
        ('stop_limit', 'Stop Limit'),
        ('take_profit', 'Take Profit'),
        ('take_profit_limit', 'Take Profit Limit'),
        ('trailing_stop', 'Trailing Stop'),
    ]
    
    ORDER_SIDES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('open', 'Open'),
        ('partially_filled', 'Partially Filled'),
        ('filled', 'Filled'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    TIME_IN_FORCE = [
        ('GTC', 'Good Till Cancelled'),
        ('IOC', 'Immediate Or Cancel'),
        ('FOK', 'Fill Or Kill'),
        ('DAY', 'Day'),
        ('GTD', 'Good Till Date'),
    ]
    
    # Basic order information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=100, unique=True)
    exchange_order_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Trading pair and order details
    trading_pair = models.CharField(max_length=20)  # e.g., BTC/USD
    base_currency = models.CharField(max_length=10)
    quote_currency = models.CharField(max_length=10)
    
    # Order specifications
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES)
    side = models.CharField(max_length=4, choices=ORDER_SIDES)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    stop_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    take_profit_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    # Order execution
    time_in_force = models.CharField(max_length=3, choices=TIME_IN_FORCE, default='GTC')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    
    # Filled quantities and prices
    filled_quantity = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    average_fill_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    total_quote_amount = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    
    # Fees
    fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    fee_currency = models.CharField(max_length=10, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    filled_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Additional fields
    is_post_only = models.BooleanField(default=False)
    reduce_only = models.BooleanField(default=False)
    iceberg_quantity = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    client_order_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Notes and metadata
    notes = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['trading_pair', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['order_id']),
        ]
    
    def __str__(self):
        return f"{self.order_id} - {self.side} {self.quantity} {self.base_currency} @ {self.price or 'MARKET'}"
    
    @property
    def remaining_quantity(self):
        """Calculate remaining unfilled quantity"""
        return self.quantity - self.filled_quantity
    
    @property
    def is_filled(self):
        """Check if order is completely filled"""
        return self.filled_quantity >= self.quantity
    
    @property
    def is_partially_filled(self):
        """Check if order is partially filled"""
        return 0 < self.filled_quantity < self.quantity
    
    @property
    def is_active(self):
        """Check if order is still active"""
        return self.status in ['pending', 'open', 'partially_filled']

class OrderFill(models.Model):
    """Model for individual order fills"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='fills')
    fill_id = models.CharField(max_length=100, unique=True)
    exchange_fill_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Fill details
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    quote_amount = models.DecimalField(max_digits=20, decimal_places=8)
    
    # Fees
    fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    fee_currency = models.CharField(max_length=10, null=True, blank=True)
    
    # Timestamps
    filled_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-filled_at']
        indexes = [
            models.Index(fields=['order', 'filled_at']),
            models.Index(fields=['fill_id']),
        ]
    
    def __str__(self):
        return f"{self.fill_id} - {self.quantity} @ {self.price}"

class OrderBook(models.Model):
    """Model for order book snapshots"""
    
    trading_pair = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    
    # Order book data
    bids = models.JSONField()  # List of [price, quantity] pairs
    asks = models.JSONField()  # List of [price, quantity] pairs
    
    # Metadata
    sequence_number = models.BigIntegerField(null=True, blank=True)
    exchange = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['trading_pair', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.trading_pair} - {self.timestamp}"

class OrderTemplate(models.Model):
    """Model for reusable order templates"""
    
    TEMPLATE_TYPES = [
        ('basic', 'Basic Order'),
        ('bracket', 'Bracket Order'),
        ('oco', 'One-Cancels-Other'),
        ('trailing_stop', 'Trailing Stop'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_templates')
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    description = models.TextField(blank=True)
    
    # Template configuration
    trading_pair = models.CharField(max_length=20)
    order_type = models.CharField(max_length=20, choices=Order.ORDER_TYPES)
    side = models.CharField(max_length=4, choices=Order.ORDER_SIDES)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price_offset = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # Percentage offset
    stop_loss_offset = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    take_profit_offset = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Advanced settings
    time_in_force = models.CharField(max_length=3, choices=Order.TIME_IN_FORCE, default='GTC')
    is_post_only = models.BooleanField(default=False)
    reduce_only = models.BooleanField(default=False)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.template_type}"

class OrderAlgo(models.Model):
    """Model for algorithmic order types"""
    
    ALGO_TYPES = [
        ('twap', 'Time-Weighted Average Price'),
        ('vwap', 'Volume-Weighted Average Price'),
        ('iceberg', 'Iceberg'),
        ('dca', 'Dollar Cost Averaging'),
        ('grid', 'Grid Trading'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='algo_order')
    algo_type = models.CharField(max_length=20, choices=ALGO_TYPES)
    
    # Algo-specific parameters
    parameters = models.JSONField(default=dict)
    
    # Execution tracking
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_chunks = models.IntegerField(default=1)
    executed_chunks = models.IntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.algo_type} - {self.order.order_id}"
