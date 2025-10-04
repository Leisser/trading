from rest_framework import serializers
from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    """Serializer for Trade model."""
    
    class Meta:
        model = Trade
        fields = [
            'id', 'user', 'symbol', 'side', 'amount', 'price', 
            'total', 'status', 'order_type', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        """Validate trade amount."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_price(self, value):
        """Validate trade price."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value
