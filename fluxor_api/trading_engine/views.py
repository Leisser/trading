from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderListView(generics.ListAPIView):
    """List all orders for the authenticated user."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return empty queryset for now - will be implemented when models are created
        return []
    
    def get_serializer_class(self):
        from .serializers import OrderSerializer
        return OrderSerializer


class OrderDetailView(generics.RetrieveAPIView):
    """Retrieve a specific order."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return empty queryset for now - will be implemented when models are created
        return []
    
    def get_serializer_class(self):
        from .serializers import OrderSerializer
        return OrderSerializer


class CreateOrderView(generics.CreateAPIView):
    """Create a new order."""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        from .serializers import OrderSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateOrderView(generics.UpdateAPIView):
    """Update an existing order."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return empty queryset for now - will be implemented when models are created
        return []
    
    def get_serializer_class(self):
        from .serializers import OrderSerializer
        return OrderSerializer


class CancelOrderView(generics.DestroyAPIView):
    """Cancel an order."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return empty queryset for now - will be implemented when models are created
        return []


class PositionListView(generics.ListAPIView):
    """List all positions for the authenticated user."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return empty queryset for now - will be implemented when models are created
        return []
    
    def get_serializer_class(self):
        from .serializers import PositionSerializer
        return PositionSerializer


class PositionDetailView(generics.RetrieveAPIView):
    """Retrieve a specific position."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return empty queryset for now - will be implemented when models are created
        return []
    
    def get_serializer_class(self):
        from .serializers import PositionSerializer
        return PositionSerializer
