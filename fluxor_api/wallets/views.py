from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from decimal import Decimal
import uuid

from .models import Wallet, MultiCurrencyWallet, CryptoBalance
from .serializers import (
    WalletSerializer, WalletBalanceSerializer, DepositRequestSerializer, 
    WithdrawalRequestSerializer, MultiCurrencyWalletSerializer, CryptoBalanceSerializer
)
from trades.models import UserDepositRequest, Withdrawal, DepositWallet, Cryptocurrency


class UserWalletView(APIView):
    """Get user's wallet information"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            wallet, created = Wallet.objects.get_or_create(
                user=request.user,
                defaults={'address': f'wallet_{request.user.id}', 'balance': Decimal('0')}
            )
            serializer = WalletSerializer(wallet)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserBalanceView(APIView):
    """Get user's current balance"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            wallet, created = Wallet.objects.get_or_create(
                user=request.user,
                defaults={'address': f'wallet_{request.user.id}', 'balance': Decimal('0')}
            )

            data = {
                'balance': wallet.balance,
                'address': wallet.address,
                'is_active': wallet.is_active
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepositRequestView(APIView):
    """Create a deposit request"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()
            data['user'] = request.user.id

            serializer = DepositRequestSerializer(data=data)
            if serializer.is_valid():
                deposit_request = serializer.save()
                return Response({
                    'id': deposit_request.id,
                    'message': 'Deposit request created successfully',
                    'status': 'pending',
                    'deposit': DepositRequestSerializer(deposit_request).data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Get user's deposit requests"""
        try:
            deposits = UserDepositRequest.objects.filter(user=request.user).select_related('deposit_wallet__cryptocurrency').order_by('-created_at')
            serializer = DepositRequestSerializer(deposits, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WithdrawalRequestView(APIView):
    """Create a withdrawal request"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Check if user has sufficient balance
            wallet = get_object_or_404(Wallet, user=request.user)
            amount = Decimal(str(request.data.get('amount', 0)))

            if amount <= 0:
                return Response({'error': 'Amount must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

            if wallet.balance < amount:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

            # Create withdrawal request
            withdrawal = Withdrawal.objects.create(
                user=request.user,
                amount=amount,
                destination_address=request.data.get('destination_address'),
                cryptocurrency=request.data.get('cryptocurrency', 'USD'),
                status='pending'
            )

            return Response({
                'id': withdrawal.id,
                'message': 'Withdrawal request created successfully',
                'status': 'pending'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Get user's withdrawal requests"""
        try:
            withdrawals = Withdrawal.objects.filter(user=request.user).order_by('-created_at')
            serializer = WithdrawalRequestSerializer(withdrawals, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepositWalletsView(APIView):
    """Get available deposit wallets for different cryptocurrencies"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Get only active deposit wallets
            deposit_wallets = DepositWallet.objects.filter(is_active=True).select_related('cryptocurrency')
            
            # Build response data
            data = []
            for wallet in deposit_wallets:
                data.append({
                    'id': wallet.id,
                    'cryptocurrency': wallet.cryptocurrency.symbol,
                    'cryptocurrency_name': wallet.cryptocurrency.name,
                    'wallet_address': wallet.wallet_address,
                    'wallet_name': wallet.wallet_name,
                    'is_primary': wallet.is_primary,
                    'network': wallet.cryptocurrency.blockchain_network or 'mainnet',
                    'min_confirmations': wallet.min_confirmation_blocks
                })
            
            return Response({
                'wallets': data,
                'count': len(data)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def wallet_balance(request):
    """Get user's wallet balance - Returns total USD balance from multi-currency wallet"""
    try:
        # Try to get multi-currency wallet first (preferred)
        try:
            multi_wallet = MultiCurrencyWallet.objects.get(user=request.user)
            total_balance_usd = multi_wallet.get_total_balance_usd()
        except MultiCurrencyWallet.DoesNotExist:
            # Fall back to legacy wallet if multi-currency wallet doesn't exist
            wallet, created = Wallet.objects.get_or_create(
                user=request.user,
                defaults={'address': f'wallet_{request.user.id}', 'balance': Decimal('0')}
            )
            total_balance_usd = wallet.balance
        
        return Response({
            'balance': total_balance_usd,
            'total_balance_usd': total_balance_usd
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MultiCurrencyWalletView(APIView):
    """Get or create user's multi-currency wallet"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Get or create multi-currency wallet
            wallet, created = MultiCurrencyWallet.objects.get_or_create(
                user=request.user,
                defaults={
                    'wallet_address': f'MCW_{uuid.uuid4().hex[:16].upper()}',
                    'is_active': True
                }
            )
            
            serializer = MultiCurrencyWalletSerializer(wallet)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CryptoBalanceListView(APIView):
    """Get user's cryptocurrency balances"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Get or create multi-currency wallet
            wallet, created = MultiCurrencyWallet.objects.get_or_create(
                user=request.user,
                defaults={
                    'wallet_address': f'MCW_{uuid.uuid4().hex[:16].upper()}',
                    'is_active': True
                }
            )
            
            # Get all balances for this wallet
            balances = CryptoBalance.objects.filter(wallet=wallet).select_related('cryptocurrency')
            serializer = CryptoBalanceSerializer(balances, many=True)
            
            return Response({
                'wallet_address': wallet.wallet_address,
                'total_balance_usd': wallet.get_total_balance_usd(),
                'balances': serializer.data,
                'count': balances.count()
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddCryptoBalanceView(APIView):
    """Add or update cryptocurrency balance in wallet"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Get or create multi-currency wallet
            wallet, created = MultiCurrencyWallet.objects.get_or_create(
                user=request.user,
                defaults={
                    'wallet_address': f'MCW_{uuid.uuid4().hex[:16].upper()}',
                    'is_active': True
                }
            )
            
            cryptocurrency_id = request.data.get('cryptocurrency')
            amount = Decimal(str(request.data.get('amount', 0)))
            
            if amount <= 0:
                return Response({'error': 'Amount must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get cryptocurrency
            try:
                cryptocurrency = Cryptocurrency.objects.get(id=cryptocurrency_id)
            except Cryptocurrency.DoesNotExist:
                return Response({'error': 'Cryptocurrency not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Get or create balance
            crypto_balance, created = CryptoBalance.objects.get_or_create(
                wallet=wallet,
                cryptocurrency=cryptocurrency,
                defaults={'balance': amount, 'total_deposited': amount}
            )
            
            if not created:
                # Update existing balance
                crypto_balance.balance += amount
                crypto_balance.total_deposited += amount
                crypto_balance.save()
            
            serializer = CryptoBalanceSerializer(crypto_balance)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
