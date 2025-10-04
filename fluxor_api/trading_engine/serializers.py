from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    """Serializer for Order model."""
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True)
    symbol = serializers.CharField(max_length=20)
    side = serializers.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    price = serializers.DecimalField(max_digits=20, decimal_places=8, required=False)
    order_type = serializers.ChoiceField(choices=[('market', 'Market'), ('limit', 'Limit')])
    status = serializers.CharField(max_length=20, default='pending')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def validate_amount(self, value):
        """Validate order amount."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_price(self, value):
        """Validate order price."""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class PositionSerializer(serializers.Serializer):
    """Serializer for Position model."""
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True)
    symbol = serializers.CharField(max_length=20)
    side = serializers.ChoiceField(choices=[('long', 'Long'), ('short', 'Short')])
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    entry_price = serializers.DecimalField(max_digits=20, decimal_places=8)
    current_price = serializers.DecimalField(max_digits=20, decimal_places=8, required=False)
    pnl = serializers.DecimalField(max_digits=20, decimal_places=8, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)