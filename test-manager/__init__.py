# для того, чтобы используемые в проекте Django shared_task-и знали, какой экземпляр Celery должен использоваться
from .celery import app as celery_app

__all__ = ('celery_app',)
