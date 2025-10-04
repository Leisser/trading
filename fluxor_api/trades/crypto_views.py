from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Trade

User = get_user_model()


class TradeListView(generics.ListAPIView):
    """List all trades for the authenticated user."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        from .serializers import TradeSerializer
        return TradeSerializer


class TradeDetailView(generics.RetrieveAPIView):
    """Retrieve a specific trade."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        from .serializers import TradeSerializer
        return TradeSerializer


class CreateTradeView(generics.CreateAPIView):
    """Create a new trade."""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        from .serializers import TradeSerializer
        return TradeSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateTradeView(generics.UpdateAPIView):
    """Update an existing trade."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        from .serializers import TradeSerializer
        return TradeSerializer


class DeleteTradeView(generics.DestroyAPIView):
    """Delete a trade."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)
