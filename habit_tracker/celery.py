# habit_tracker/celery.py
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

app = Celery("habit_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Таймзона — работаем по Москве, хранение можно оставить в UTC
app.conf.timezone = settings.TIME_ZONE  # "Europe/Moscow" из .env
app.conf.enable_utc = True
