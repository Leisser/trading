from rest_framework import serializers
from decimal import Decimal
from .models import Wallet, MultiCurrencyWallet, CryptoBalance
from trades.models import UserDepositRequest, Withdrawal, DepositWallet, Cryptocurrency
from accounts.models import User


class WalletSerializer(serializers.ModelSerializer):
    """Serializer for user wallets"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'user_email', 'user_name', 'address', 'balance', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username or obj.user.email


class WalletBalanceSerializer(serializers.Serializer):
    """Serializer for wallet balance information"""
    balance = serializers.DecimalField(max_digits=20, decimal_places=8)
    address = serializers.CharField()
    is_active = serializers.BooleanField()


class DepositRequestSerializer(serializers.ModelSerializer):
    """Serializer for deposit requests"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)
    cryptocurrency_name = serializers.CharField(source='deposit_wallet.cryptocurrency.name', read_only=True)
    cryptocurrency_symbol = serializers.CharField(source='deposit_wallet.cryptocurrency.symbol', read_only=True)
    wallet_name = serializers.CharField(source='deposit_wallet.wallet_name', read_only=True)
    
    class Meta:
        model = UserDepositRequest
        fields = [
            'id', 'user', 'user_email', 'user_name', 'amount', 'deposit_wallet',
            'cryptocurrency_name', 'cryptocurrency_symbol', 'wallet_name',
            'transaction_hash', 'from_address', 'status', 
            'review_notes', 'created_at', 'confirmed_at'
        ]
        read_only_fields = ['id', 'status', 'review_notes', 'created_at', 'confirmed_at']
    
    def get_user_name(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username or obj.user.email
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_deposit_wallet(self, value):
        if not value or not value.is_active:
            raise serializers.ValidationError("Invalid or inactive deposit wallet")
        return value


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    """Serializer for withdrawal requests"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)
    cryptocurrency_name = serializers.CharField(source='cryptocurrency.name', read_only=True)
    
    class Meta:
        model = Withdrawal
        fields = [
            'id', 'user', 'user_email', 'user_name', 'amount', 'cryptocurrency',
            'cryptocurrency_name', 'destination_address', 'transaction_hash', 
            'status', 'admin_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'transaction_hash', 'admin_notes', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username or obj.user.email
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_destination_address(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Destination address is required")
        return value.strip()


class DepositWalletSerializer(serializers.ModelSerializer):
    """Serializer for deposit wallets"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    cryptocurrency_name = serializers.CharField(source='cryptocurrency.name', read_only=True)
    
    class Meta:
        model = DepositWallet
        fields = [
            'id', 'cryptocurrency', 'cryptocurrency_symbol', 'cryptocurrency_name',
            'wallet_address', 'wallet_name', 'is_active', 'is_primary',
            'current_balance', 'total_received', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'current_balance', 'total_received', 'created_at', 'updated_at']


class UserDepositRequestAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for deposit requests with additional fields"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)
    cryptocurrency_name = serializers.CharField(source='cryptocurrency.name', read_only=True)
    
    class Meta:
        model = UserDepositRequest
        fields = [
            'id', 'user', 'user_email', 'user_name', 'amount', 'cryptocurrency',
            'cryptocurrency_name', 'wallet_address', 'transaction_hash', 'status',
            'admin_notes', 'approved_by', 'approved_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username or obj.user.email


class WithdrawalAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for withdrawal requests with additional fields"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)
    cryptocurrency_name = serializers.CharField(source='cryptocurrency.name', read_only=True)
    
    class Meta:
        model = Withdrawal
        fields = [
            'id', 'user', 'user_email', 'user_name', 'amount', 'cryptocurrency',
            'cryptocurrency_name', 'destination_address', 'transaction_hash',
            'status', 'admin_notes', 'approved_by', 'approved_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username or obj.user.email


class CryptoBalanceSerializer(serializers.ModelSerializer):
    """Serializer for cryptocurrency balances"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    cryptocurrency_name = serializers.CharField(source='cryptocurrency.name', read_only=True)
    current_price = serializers.DecimalField(source='cryptocurrency.current_price', max_digits=20, decimal_places=8, read_only=True)
    available_balance = serializers.DecimalField(max_digits=20, decimal_places=8, read_only=True)
    balance_usd = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    
    class Meta:
        model = CryptoBalance
        fields = [
            'id', 'cryptocurrency', 'cryptocurrency_symbol', 'cryptocurrency_name',
            'balance', 'locked_balance', 'available_balance', 'current_price',
            'balance_usd', 'total_deposited', 'total_withdrawn',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MultiCurrencyWalletSerializer(serializers.ModelSerializer):
    """Serializer for multi-currency wallet"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    balances = CryptoBalanceSerializer(many=True, read_only=True)
    total_balance_usd = serializers.SerializerMethodField()
    
    class Meta:
        model = MultiCurrencyWallet
        fields = [
            'id', 'user', 'user_email', 'wallet_address', 'is_active',
            'balances', 'total_balance_usd', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'wallet_address', 'created_at', 'updated_at']
    
    def get_total_balance_usd(self, obj):
        return obj.get_total_balance_usd()


class WalletTransactionSerializer(serializers.Serializer):
    """Serializer for wallet transactions"""
    id = serializers.IntegerField()
    type = serializers.CharField()  # 'deposit' or 'withdrawal'
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    cryptocurrency = serializers.CharField()
    status = serializers.CharField()
    transaction_hash = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    
    def to_representation(self, instance):
        """Convert model instance to serialized data"""
        if hasattr(instance, 'destination_address'):
            # This is a withdrawal
            return {
                'id': instance.id,
                'type': 'withdrawal',
                'amount': instance.amount,
                'cryptocurrency': instance.cryptocurrency,
                'status': instance.status,
                'transaction_hash': instance.transaction_hash,
                'destination_address': instance.destination_address,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at
            }
        else:
            # This is a deposit
            return {
                'id': instance.id,
                'type': 'deposit',
                'amount': instance.amount,
                'cryptocurrency': instance.cryptocurrency,
                'status': instance.status,
                'transaction_hash': instance.transaction_hash,
                'wallet_address': instance.wallet_address,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at
            }
