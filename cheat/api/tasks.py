from celery import shared_task
from users.models import CustomUser

# celery -A config.celery worker --loglevel=INFO
# celery -A config.celery beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A config worker --loglevel=info

# FLOWER celery -A config flower --port=5554


@shared_task(bind=True)
def test_func(self):
    for i in range(100):
        CustomUser.objects.create(email=f"vasdasd{i}@gmail.com", password="en1996ru")
    return "DONE"
