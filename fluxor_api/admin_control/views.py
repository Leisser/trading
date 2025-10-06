"""
Admin Control API Views for Profit/Loss Scenarios and Trading Settings
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Q, Count, Sum
from datetime import datetime, timedelta
from decimal import Decimal

from .models import TradingSettings, ProfitLossScenario, ScenarioExecution
from .serializers import (
    TradingSettingsSerializer, ProfitLossScenarioSerializer, CreateProfitLossScenarioSerializer,
    ScenarioExecutionSerializer, ExecuteScenarioSerializer, TradingSettingsUpdateSerializer
)
from investments.models import Investment
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow admins to modify data"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_staff


class TradingSettingsView(APIView):
    """Manage global trading settings"""
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        """Get current trading settings"""
        try:
            settings = TradingSettings.objects.first()
            if not settings:
                # Create default settings if none exist
                settings = TradingSettings.objects.create()
            
            serializer = TradingSettingsSerializer(settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        request_body=TradingSettingsUpdateSerializer,
        responses={200: TradingSettingsSerializer}
    )
    def put(self, request):
        """Update trading settings"""
        try:
            settings = TradingSettings.objects.first()
            if not settings:
                settings = TradingSettings.objects.create()
            
            serializer = TradingSettingsUpdateSerializer(settings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                response_serializer = TradingSettingsSerializer(settings)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProfitLossScenarioListView(generics.ListCreateAPIView):
    """List and create profit/loss scenarios"""
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return ProfitLossScenario.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProfitLossScenarioSerializer
        return ProfitLossScenarioSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProfitLossScenarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage individual profit/loss scenarios"""
    permission_classes = [IsAdminOrReadOnly]
    queryset = ProfitLossScenario.objects.all()
    serializer_class = ProfitLossScenarioSerializer


class ScenarioExecutionListView(generics.ListAPIView):
    """List scenario executions"""
    permission_classes = [IsAdminOrReadOnly]
    queryset = ScenarioExecution.objects.all()
    serializer_class = ScenarioExecutionSerializer


@api_view(['POST'])
@permission_classes([IsAdminOrReadOnly])
def execute_scenario(request, scenario_id):
    """Execute a profit/loss scenario"""
    try:
        scenario = ProfitLossScenario.objects.get(id=scenario_id)
        
        if not scenario.is_active and not request.data.get('force_execute', False):
            return Response(
                {'error': 'Scenario is not active. Use force_execute=true to override.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ExecuteScenarioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        dry_run = serializer.validated_data.get('dry_run', False)
        notes = serializer.validated_data.get('notes', '')
        
        # Get affected investments
        affected_investments = []
        affected_users = set()
        
        if scenario.apply_to_all_investments:
            investments = Investment.objects.filter(status='active')
        elif scenario.target_crypto_index:
            investments = Investment.objects.filter(
                crypto_index=scenario.target_crypto_index,
                status='active'
            )
        elif scenario.target_cryptocurrency:
            investments = Investment.objects.filter(
                cryptocurrency=scenario.target_cryptocurrency,
                status='active'
            )
        else:
            investments = Investment.objects.none()
        
        affected_investments = list(investments)
        affected_users = set(inv.user for inv in affected_investments)
        
        if dry_run:
            return Response({
                'message': 'Dry run completed',
                'scenario': ProfitLossScenarioSerializer(scenario).data,
                'affected_investments': len(affected_investments),
                'affected_users': len(affected_users),
                'total_value_change': sum(inv.current_value_usd for inv in affected_investments) * (scenario.percentage_change / 100)
            }, status=status.HTTP_200_OK)
        
        # Execute the scenario
        total_value_change = Decimal('0')
        successful_updates = 0
        
        for investment in affected_investments:
            try:
                # Calculate new values
                change_factor = Decimal('1') + (scenario.percentage_change / Decimal('100'))
                
                new_value_btc = investment.current_value_btc * change_factor
                new_value_usd = investment.current_value_usd * change_factor
                
                # Update investment
                investment.current_value_btc = new_value_btc
                investment.current_value_usd = new_value_usd
                investment.unrealized_pnl_btc = new_value_btc - investment.total_invested_btc
                investment.unrealized_pnl_usd = new_value_usd - investment.total_invested_usd
                
                if investment.total_invested_btc > 0:
                    investment.unrealized_pnl_percent = (investment.unrealized_pnl_btc / investment.total_invested_btc) * 100
                
                investment.save()
                successful_updates += 1
                total_value_change += investment.current_value_usd - (investment.current_value_usd / change_factor)
                
            except Exception as e:
                continue
        
        # Create execution record
        execution = ScenarioExecution.objects.create(
            scenario=scenario,
            executed_by=request.user,
            affected_investments=successful_updates,
            affected_users=len(affected_users),
            total_value_change=total_value_change,
            status='success' if successful_updates > 0 else 'failed',
            error_message=notes
        )
        
        # Update scenario
        scenario.times_executed += 1
        scenario.last_executed = timezone.now()
        
        if scenario.repeat_execution:
            scenario.next_execution = timezone.now() + timedelta(hours=scenario.repeat_interval_hours)
        
        scenario.save()
        
        return Response({
            'message': 'Scenario executed successfully',
            'execution_id': execution.id,
            'affected_investments': successful_updates,
            'affected_users': len(affected_users),
            'total_value_change': total_value_change
        }, status=status.HTTP_200_OK)
        
    except ProfitLossScenario.DoesNotExist:
        return Response(
            {'error': 'Scenario not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAdminOrReadOnly])
def activate_scenario(request, scenario_id):
    """Activate a profit/loss scenario"""
    try:
        scenario = ProfitLossScenario.objects.get(id=scenario_id)
        scenario.is_active = True
        scenario.save()
        
        serializer = ProfitLossScenarioSerializer(scenario)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except ProfitLossScenario.DoesNotExist:
        return Response(
            {'error': 'Scenario not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAdminOrReadOnly])
def deactivate_scenario(request, scenario_id):
    """Deactivate a profit/loss scenario"""
    try:
        scenario = ProfitLossScenario.objects.get(id=scenario_id)
        scenario.is_active = False
        scenario.save()
        
        serializer = ProfitLossScenarioSerializer(scenario)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except ProfitLossScenario.DoesNotExist:
        return Response(
            {'error': 'Scenario not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class AdminDashboardView(APIView):
    """Admin dashboard with system statistics"""
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        """Get admin dashboard data"""
        try:
            # Get trading settings
            settings = TradingSettings.objects.first()
            if not settings:
                settings = TradingSettings.objects.create()
            
            # Get scenario statistics
            total_scenarios = ProfitLossScenario.objects.count()
            active_scenarios = ProfitLossScenario.objects.filter(is_active=True).count()
            recent_executions = ScenarioExecution.objects.filter(
                executed_at__gte=timezone.now() - timedelta(days=7)
            ).count()
            
            # Get investment statistics
            total_investments = Investment.objects.count()
            active_investments = Investment.objects.filter(status='active').count()
            total_invested_value = Investment.objects.aggregate(
                total=Sum('total_invested_usd')
            )['total'] or Decimal('0')
            total_current_value = Investment.objects.aggregate(
                total=Sum('current_value_usd')
            )['total'] or Decimal('0')
            
            # Get user statistics
            from django.contrib.auth import get_user_model
            User = get_user_model()
            total_users = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            
            return Response({
                'trading_settings': TradingSettingsSerializer(settings).data,
                'scenario_stats': {
                    'total_scenarios': total_scenarios,
                    'active_scenarios': active_scenarios,
                    'recent_executions': recent_executions
                },
                'investment_stats': {
                    'total_investments': total_investments,
                    'active_investments': active_investments,
                    'total_invested_value': total_invested_value,
                    'total_current_value': total_current_value,
                    'total_pnl': total_current_value - total_invested_value
                },
                'user_stats': {
                    'total_users': total_users,
                    'active_users': active_users
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
