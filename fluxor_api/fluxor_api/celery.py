import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluxor_api.settings')

app = Celery('fluxor_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Import tasks from all apps
app.conf.imports = [
    'market_data.tasks',
    'order_management.tasks',
    'portfolio_management.tasks',
    'risk_management.tasks',
    'compliance.tasks',
    'alerts.tasks',
    'reports.tasks',
    'core.tasks',
]

# Celery Beat Schedule
app.conf.beat_schedule = {
    'update-market-data': {
        'task': 'market_data.tasks.update_market_data',
        'schedule': 5.0,  # Every 5 seconds
    },
    'update-price-feeds': {
        'task': 'market_data.tasks.update_price_feeds',
        'schedule': 1.0,  # Every second
    },
    'process-pending-orders': {
        'task': 'order_management.tasks.process_pending_orders',
        'schedule': 2.0,  # Every 2 seconds
    },
    'check-risk-limits': {
        'task': 'risk_management.tasks.check_risk_limits',
        'schedule': 30.0,  # Every 30 seconds
    },
    'run-compliance-checks': {
        'task': 'compliance.tasks.run_compliance_checks',
        'schedule': 300.0,  # Every 5 minutes
    },
    'process-alerts': {
        'task': 'alerts.tasks.process_alerts',
        'schedule': 10.0,  # Every 10 seconds
    },
    'generate-reports': {
        'task': 'reports.tasks.generate_scheduled_reports',
        'schedule': 3600.0,  # Every hour
    },
    'update-portfolio-values': {
        'task': 'portfolio_management.tasks.update_portfolio_values',
        'schedule': 60.0,  # Every minute
    },
    'cleanup-old-data': {
        'task': 'core.tasks.cleanup_old_data',
        'schedule': 86400.0,  # Daily
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 