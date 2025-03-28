import os
from celery import Celery

# Устанавливаем модуль настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # Автоматически найдет файлы tasks.py во всех приложениях из INSTALLED_APPS

# Опционально: настройка расписания задач через Celery Beat
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send_weekly_news_every_monday_8am': {
        'task': 'news.tasks.send_weekly_news',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # понедельник 8:00 утра
    },
}
