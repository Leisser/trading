from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import BlockchainMonitor, Transaction
from .serializers import (
    BlockchainHealthSerializer, TransactionStatusSerializer,
    NetworkStatsSerializer, BlockInfoSerializer
)

class BlockchainHealthView(APIView):
    """
    Get blockchain network health status.
    
    This endpoint provides real-time information about the Bitcoin blockchain
    network health, including connection status, sync status, and any issues.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Blockchain health status retrieved successfully",
                examples={
                    "application/json": {
                        "status": "healthy",
                        "message": "All systems operational",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "block_height": 800000,
                        "connections": 8,
                        "sync_status": "synced",
                        "last_block_time": "2024-01-01T11:55:00Z"
                    }
                }
            )
        },
        operation_description="Get current blockchain network health status"
    )
    def get(self, request):
        latest_status = BlockchainMonitor.objects.first()
        if latest_status:
            return Response({
                'status': latest_status.status,
                'message': latest_status.message,
                'timestamp': latest_status.timestamp,
                'block_height': 800000,  # Mock data
                'connections': 8,
                'sync_status': 'synced',
                'last_block_time': '2024-01-01T11:55:00Z'
            })
        return Response({
            'status': 'unknown', 
            'message': 'No health data available',
            'timestamp': None
        })

class TransactionStatusView(APIView):
    """
    Get transaction status and details.
    
    This endpoint allows users to check the status of a specific transaction
    by providing the transaction hash (txid).
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'txid',
                openapi.IN_QUERY,
                description="Transaction hash to check",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Transaction status retrieved successfully",
                examples={
                    "application/json": {
                        "txid": "abc123def456...",
                        "status": "confirmed",
                        "confirmations": 6,
                        "block_height": 800000,
                        "amount": "0.001",
                        "fee": "0.0001",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "from_address": "bc1q...",
                        "to_address": "bc1q..."
                    }
                }
            ),
            404: "Transaction not found"
        },
        operation_description="Get status and details of a specific transaction"
    )
    def get(self, request):
        txid = request.query_params.get('txid')
        if not txid:
            return Response(
                {'error': 'Transaction hash (txid) is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mock transaction data for demonstration
        transaction_data = {
            'txid': txid,
            'status': 'confirmed',
            'confirmations': 6,
            'block_height': 800000,
            'amount': '0.001',
            'fee': '0.0001',
            'timestamp': '2024-01-01T12:00:00Z',
            'from_address': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
            'to_address': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
        }
        
        return Response(transaction_data)

class NetworkStatsView(APIView):
    """
    Get Bitcoin network statistics.
    
    This endpoint provides comprehensive statistics about the Bitcoin network
    including difficulty, hash rate, mempool size, and other key metrics.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Network statistics retrieved successfully",
                examples={
                    "application/json": {
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
                }
            )
        },
        operation_description="Get comprehensive Bitcoin network statistics"
    )
    def get(self, request):
        # Mock network statistics for demonstration
        stats = {
            'current_difficulty': '12345678901234567890',
            'hash_rate': '450.5 EH/s',
            'mempool_size': 15000,
            'mempool_fees': '0.0001',
            'block_time': 600,
            'total_transactions': 800000000,
            'total_supply': '19,500,000',
            'market_cap': '900,000,000,000',
            'price_usd': '45000.00'
        }
        return Response(stats)

class BlockInfoView(APIView):
    """
    Get information about a specific block.
    
    This endpoint provides detailed information about a Bitcoin block
    including transactions, size, and other block-specific data.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'block_height',
                openapi.IN_QUERY,
                description="Block height to get information for",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Block information retrieved successfully",
                examples={
                    "application/json": {
                        "block_height": 800000,
                        "block_hash": "0000000000000000000...",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "transactions": 2500,
                        "size": 1500000,
                        "weight": 4000000,
                        "merkle_root": "abc123...",
                        "previous_block": "0000000000000000000...",
                        "next_block": "0000000000000000000...",
                        "difficulty": "12345678901234567890"
                    }
                }
            ),
            404: "Block not found"
        },
        operation_description="Get detailed information about a specific block"
    )
    def get(self, request):
        block_height = request.query_params.get('block_height')
        if not block_height:
            return Response(
                {'error': 'Block height is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            block_height = int(block_height)
        except ValueError:
            return Response(
                {'error': 'Invalid block height'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mock block data for demonstration
        block_data = {
            'block_height': block_height,
            'block_hash': '0000000000000000000abcdef1234567890abcdef1234567890abcdef123456789',
            'timestamp': '2024-01-01T12:00:00Z',
            'transactions': 2500,
            'size': 1500000,
            'weight': 4000000,
            'merkle_root': 'abc123def4567890abcdef1234567890abcdef1234567890abcdef123456789',
            'previous_block': '0000000000000000000abcdef1234567890abcdef1234567890abcdef123456788',
            'next_block': '0000000000000000000abcdef1234567890abcdef1234567890abcdef123456790',
            'difficulty': '12345678901234567890'
        }
        
        return Response(block_data)

class MempoolView(APIView):
    """
    Get current mempool information.
    
    This endpoint provides information about the current Bitcoin mempool
    including pending transactions, fees, and congestion status.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Mempool information retrieved successfully",
                examples={
                    "application/json": {
                        "mempool_size": 15000,
                        "mempool_bytes": 50000000,
                        "mempool_fees": "0.0001",
                        "pending_transactions": 15000,
                        "low_fee_transactions": 5000,
                        "medium_fee_transactions": 7000,
                        "high_fee_transactions": 3000,
                        "estimated_confirmation_time": 10
                    }
                }
            )
        },
        operation_description="Get current Bitcoin mempool information"
    )
    def get(self, request):
        # Mock mempool data for demonstration
        mempool_data = {
            'mempool_size': 15000,
            'mempool_bytes': 50000000,
            'mempool_fees': '0.0001',
            'pending_transactions': 15000,
            'low_fee_transactions': 5000,
            'medium_fee_transactions': 7000,
            'high_fee_transactions': 3000,
            'estimated_confirmation_time': 10
        }
        return Response(mempool_data)

class FeeEstimateView(APIView):
    """
    Get Bitcoin transaction fee estimates.
    
    This endpoint provides fee estimates for different confirmation times
    to help users set appropriate transaction fees.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'confirmation_target',
                openapi.IN_QUERY,
                description="Target confirmation time in blocks",
                type=openapi.TYPE_INTEGER,
                default=6
            )
        ],
        responses={
            200: openapi.Response(
                description="Fee estimates retrieved successfully",
                examples={
                    "application/json": {
                        "fastest": "0.0005",
                        "half_hour": "0.0003",
                        "hour": "0.0002",
                        "economy": "0.0001",
                        "minimum": "0.00001"
                    }
                }
            )
        },
        operation_description="Get Bitcoin transaction fee estimates for different confirmation times"
    )
    def get(self, request):
        # Mock fee estimates for demonstration
        fee_estimates = {
            'fastest': '0.0005',
            'half_hour': '0.0003',
            'hour': '0.0002',
            'economy': '0.0001',
            'minimum': '0.00001'
        }
        return Response(fee_estimates) 