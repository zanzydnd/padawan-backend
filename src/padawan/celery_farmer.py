import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'padawan.settings')

celery_app = Celery('padawan')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks(packages=['app'])

celery_app.conf.task_routes = {
    'web.*': {'queue': 'web_queue'},
    'remote.*': {'queue': 'remote_queue'},
}
