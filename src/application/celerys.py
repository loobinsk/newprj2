from celery import Celery
from celery.schedules import crontab

from datetime import timedelta

app = Celery('application')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'import-catalog-from-ftp-every-10-minutes': {
        'task': 'import_catalog_from_ftp',
        'schedule': timedelta(minutes=15),
    },
}
