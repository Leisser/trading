from rest_framework import serializers
from .models import BlockchainMonitor, Transaction

class BlockchainHealthSerializer(serializers.ModelSerializer):
    """
    Serializer for blockchain health status.
    
    Example Response:
    {
        "status": "healthy",
        "message": "All systems operational",
        "timestamp": "2024-01-01T12:00:00Z",
        "block_height": 800000,
        "connections": 8,
        "sync_status": "synced"
    }
    """
    class Meta:
        model = BlockchainMonitor
        fields = ['status', 'message', 'timestamp']

class TransactionStatusSerializer(serializers.Serializer):
    """
    Serializer for transaction status information.
    
    Example Response:
    {
        "txid": "abc123def456...",
        "status": "confirmed",
        "confirmations": 6,
        "block_height": 800000,
        "amount": "0.001",
        "fee": "0.0001",
        "timestamp": "2024-01-01T12:00:00Z"
    }
    """
    txid = serializers.CharField(help_text="Transaction hash")
    status = serializers.CharField(help_text="Transaction status")
    confirmations = serializers.IntegerField(help_text="Number of confirmations")
    block_height = serializers.IntegerField(help_text="Block height where transaction was included")
    amount = serializers.CharField(help_text="Transaction amount in BTC")
    fee = serializers.CharField(help_text="Transaction fee in BTC")
    timestamp = serializers.DateTimeField(help_text="Transaction timestamp")
    from_address = serializers.CharField(help_text="Source address")
    to_address = serializers.CharField(help_text="Destination address")

class NetworkStatsSerializer(serializers.Serializer):
    """
    Serializer for Bitcoin network statistics.
    
    Example Response:
    {
        "current_difficulty": "12345678901234567890",
        "hash_rate": "450.5 EH/s",
        "mempool_size": 15000,
        "mempool_fees": "0.0001",
        "block_time": 600,
        "total_transactions": 800000000,
        "total_supply": "19,500,000",
        "market_cap": "900,000,000,000",
        "price_usd": "45000.00"
    }
    """
    current_difficulty = serializers.CharField(help_text="Current network difficulty")
    hash_rate = serializers.CharField(help_text="Network hash rate")
    mempool_size = serializers.IntegerField(help_text="Number of transactions in mempool")
    mempool_fees = serializers.CharField(help_text="Current mempool fee rate")
    block_time = serializers.IntegerField(help_text="Average block time in seconds")
    total_transactions = serializers.IntegerField(help_text="Total number of transactions")
    total_supply = serializers.CharField(help_text="Total Bitcoin supply")
    market_cap = serializers.CharField(help_text="Market capitalization in USD")
    price_usd = serializers.CharField(help_text="Current Bitcoin price in USD")

class BlockInfoSerializer(serializers.Serializer):
    """
    Serializer for block information.
    
    Example Response:
    {
        "block_height": 800000,
        "block_hash": "0000000000000000000...",
        "timestamp": "2024-01-01T12:00:00Z",
        "transactions": 2500,
        "size": 1500000,
        "weight": 4000000,
        "merkle_root": "abc123...",
        "difficulty": "12345678901234567890"
    }
    """
    block_height = serializers.IntegerField(help_text="Block height")
    block_hash = serializers.CharField(help_text="Block hash")
    timestamp = serializers.DateTimeField(help_text="Block timestamp")
    transactions = serializers.IntegerField(help_text="Number of transactions in block")
    size = serializers.IntegerField(help_text="Block size in bytes")
    weight = serializers.IntegerField(help_text="Block weight")
    merkle_root = serializers.CharField(help_text="Merkle root hash")
    previous_block = serializers.CharField(help_text="Previous block hash")
    next_block = serializers.CharField(help_text="Next block hash")
    difficulty = serializers.CharField(help_text="Block difficulty")

class MempoolSerializer(serializers.Serializer):
    """
    Serializer for mempool information.
    
    Example Response:
    {
        "mempool_size": 15000,
        "mempool_bytes": 50000000,
        "mempool_fees": "0.0001",
        "pending_transactions": 15000,
        "low_fee_transactions": 5000,
        "medium_fee_transactions": 7000,
        "high_fee_transactions": 3000,
        "estimated_confirmation_time": 10
    }
    """
    mempool_size = serializers.IntegerField(help_text="Number of transactions in mempool")
    mempool_bytes = serializers.IntegerField(help_text="Mempool size in bytes")
    mempool_fees = serializers.CharField(help_text="Current mempool fee rate")
    pending_transactions = serializers.IntegerField(help_text="Total pending transactions")
    low_fee_transactions = serializers.IntegerField(help_text="Low fee transactions")
    medium_fee_transactions = serializers.IntegerField(help_text="Medium fee transactions")
    high_fee_transactions = serializers.IntegerField(help_text="High fee transactions")
    estimated_confirmation_time = serializers.IntegerField(help_text="Estimated confirmation time in minutes")

class FeeEstimateSerializer(serializers.Serializer):
    """
    Serializer for fee estimates.
    
    Example Response:
    {
        "fastest": "0.0005",
        "half_hour": "0.0003",
        "hour": "0.0002",
        "economy": "0.0001",
        "minimum": "0.00001"
    }
    """
    fastest = serializers.CharField(help_text="Fee for fastest confirmation")
    half_hour = serializers.CharField(help_text="Fee for confirmation within 30 minutes")
    hour = serializers.CharField(help_text="Fee for confirmation within 1 hour")
    economy = serializers.CharField(help_text="Fee for economy confirmation")
    minimum = serializers.CharField(help_text="Minimum fee") 