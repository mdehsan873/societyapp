import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocietyManagementApplication.settings")
app = Celery("SocietyManagementApplication")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()