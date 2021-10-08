import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final.settings')

app = Celery('final',
             broker='amqp://',
             backend='django-db',
             )

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
