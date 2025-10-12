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

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'auto-close-due-trades': {
        'task': 'trades.tasks.auto_close_due_trades',
        'schedule': 60.0,  # Run every 60 seconds
    },
    'cleanup-old-market-data': {
        'task': 'trades.tasks.cleanup_old_market_data',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
