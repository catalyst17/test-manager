# test-manager/celery.py

import os

from celery import Celery

# устанавливает модуль настроек проекта Django для приложений Celery, используемый по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test-manager.settings')

app = Celery('test-manager')

# позволяет конфигурировать Celery в файле конфигураций Django-проекта
app.config_from_object('django.conf:settings', namespace='CELERY')

# делает задачи, описанные в других модулях, доступными для данного экземпляра Celery приложения
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
