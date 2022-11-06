from celery import shared_task
from loguru import logger

# celery -A config.celery worker --loglevel=INFO
# celery -A config.celery beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A config worker --loglevel=info

# FLOWER celery -A config flower --port=5554
# DRAMATIQ


@shared_task(bind=True)
def test_func(self, *args, **kwargs):
    logger.debug(kwargs)
    """ for i in range(100):
        print(f"{i}")
        # CustomUser.objects.create(email=f"vasdasd{i}@gmail.com", password="en1996ru") """
    return "DONE"
