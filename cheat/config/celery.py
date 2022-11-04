import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("hello", broker=settings.CELERY_BROKER_URL)

app.autodiscover_tasks()


@app.task(bind=True)
def hello():
    print("asdaskhdbasdbjadbhasdb")
    return "hello world"
