from django.db import models
from django.conf import settings
from decimal import Decimal
import uuid

class BlockchainMonitor(models.Model):
    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.status} - {self.timestamp}"

class Transaction(models.Model):
    """
    Model for tracking blockchain transactions
    """
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('fee', 'Fee'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic transaction info
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tx_hash = models.CharField(max_length=255, unique=True, help_text="Blockchain transaction hash")
    block_height = models.IntegerField(null=True, blank=True, help_text="Block height where transaction was included")
    
    # Transaction details
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=8, help_text="Transaction amount in BTC")
    fee = models.DecimalField(max_digits=20, decimal_places=8, default=0, help_text="Transaction fee in BTC")
    
    # Addresses
    from_address = models.CharField(max_length=255, blank=True, help_text="Source address")
    to_address = models.CharField(max_length=255, blank=True, help_text="Destination address")
    
    # Status and confirmations
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    confirmations = models.IntegerField(default=0, help_text="Number of confirmations")
    
    # Timestamps
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Transaction timestamp")
    confirmed_at = models.DateTimeField(null=True, blank=True, help_text="When transaction was confirmed")
    
    # Additional metadata
    notes = models.TextField(blank=True, help_text="Additional notes about the transaction")
    raw_data = models.JSONField(default=dict, help_text="Raw transaction data from blockchain")
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['tx_hash']),
            models.Index(fields=['status']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} BTC - {self.status}"
    
    @property
    def total_amount(self):
        """Total amount including fee"""
        return self.amount + self.fee
    
    def is_confirmed(self):
        """Check if transaction is confirmed (6+ confirmations)"""
        return self.confirmations >= 6
    
    def update_confirmations(self, new_confirmations):
        """Update confirmation count and status"""
        self.confirmations = new_confirmations
        if new_confirmations >= 6 and self.status == 'pending':
            self.status = 'confirmed'
            from django.utils import timezone
            self.confirmed_at = timezone.now()
        self.save()

class Block(models.Model):
    """
    Model for tracking blockchain blocks
    """
    block_height = models.IntegerField(unique=True, help_text="Block height")
    block_hash = models.CharField(max_length=255, unique=True, help_text="Block hash")
    previous_block_hash = models.CharField(max_length=255, blank=True, help_text="Previous block hash")
    merkle_root = models.CharField(max_length=255, help_text="Merkle root")
    
    # Block details
    timestamp = models.DateTimeField(help_text="Block timestamp")
    difficulty = models.DecimalField(max_digits=20, decimal_places=8, help_text="Block difficulty")
    nonce = models.BigIntegerField(help_text="Block nonce")
    
    # Size and transactions
    size = models.IntegerField(help_text="Block size in bytes")
    weight = models.IntegerField(help_text="Block weight")
    transaction_count = models.IntegerField(default=0, help_text="Number of transactions in block")
    
    # Mining info
    miner_address = models.CharField(max_length=255, blank=True, help_text="Miner address")
    block_reward = models.DecimalField(max_digits=20, decimal_places=8, help_text="Block reward in BTC")
    
    class Meta:
        ordering = ['-block_height']
        indexes = [
            models.Index(fields=['block_height']),
            models.Index(fields=['block_hash']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"Block {self.block_height} - {self.block_hash[:16]}..."

class MempoolTransaction(models.Model):
    """
    Model for tracking transactions in the mempool
    """
    tx_hash = models.CharField(max_length=255, unique=True, help_text="Transaction hash")
    fee_rate = models.DecimalField(max_digits=20, decimal_places=8, help_text="Fee rate in sat/vB")
    fee = models.DecimalField(max_digits=20, decimal_places=8, help_text="Total fee in BTC")
    size = models.IntegerField(help_text="Transaction size in bytes")
    weight = models.IntegerField(help_text="Transaction weight")
    
    # Timestamps
    first_seen = models.DateTimeField(auto_now_add=True, help_text="When transaction was first seen")
    last_updated = models.DateTimeField(auto_now=True, help_text="Last update timestamp")
    
    # Status
    is_confirmed = models.BooleanField(default=False, help_text="Whether transaction has been confirmed")
    confirmed_in_block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-fee_rate']
        indexes = [
            models.Index(fields=['tx_hash']),
            models.Index(fields=['fee_rate']),
            models.Index(fields=['first_seen']),
        ]
    
    def __str__(self):
        return f"Mempool TX - {self.tx_hash[:16]}... - {self.fee_rate} sat/vB"

class NetworkStats(models.Model):
    """
    Model for tracking network statistics
    """
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Stats timestamp")
    
    # Network metrics
    current_difficulty = models.DecimalField(max_digits=20, decimal_places=8, help_text="Current network difficulty")
    hash_rate = models.DecimalField(max_digits=20, decimal_places=2, help_text="Network hash rate in EH/s")
    block_time = models.IntegerField(help_text="Average block time in seconds")
    
    # Mempool metrics
    mempool_size = models.IntegerField(help_text="Number of transactions in mempool")
    mempool_bytes = models.BigIntegerField(help_text="Mempool size in bytes")
    mempool_fee_rate = models.DecimalField(max_digits=20, decimal_places=8, help_text="Current mempool fee rate")
    
    # Price and market data
    btc_price_usd = models.DecimalField(max_digits=10, decimal_places=2, help_text="Bitcoin price in USD")
    market_cap = models.DecimalField(max_digits=15, decimal_places=2, help_text="Market capitalization")
    volume_24h = models.DecimalField(max_digits=15, decimal_places=2, help_text="24h trading volume")
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"Network Stats - {self.timestamp} - Difficulty: {self.current_difficulty}" 