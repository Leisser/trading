import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluxor_api.settings')

app = Celery('fluxor_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure periodic tasks (Celery Beat)
app.conf.beat_schedule = {
    'cleanup-old-chart-data': {
        'task': 'core.tasks.cleanup_old_chart_data',
        'schedule': crontab(minute=0),  # Run every hour at minute 0
    },
    'generate-initial-chart-data': {
        'task': 'core.tasks.generate_initial_chart_data',
        'schedule': crontab(minute=5, hour=0),  # Run daily at 00:05
    },
    'update-active-trades': {
        'task': 'trades.tasks.update_active_trades',
        'schedule': 5.0,  # Run every 5 seconds
    },
}
