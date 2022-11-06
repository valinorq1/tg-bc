from asgiref.sync import async_to_sync
from celery import shared_task
from loguru import logger
from session.models import Session
from users.models import CommentTask, ReactionTask, SubscribeTask, ViewTask, VotingTask

# celery -A config.celery worker --loglevel=INFO
# celery -A config.celery beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A config worker --loglevel=info

# FLOWER celery -A config flower --port=5554
# DRAMATIQ


@shared_task(bind=True)
def views_task(self, *args, **kwargs):
    logger.debug(kwargs)
    return "views_task DONE"


@shared_task(bind=True)
def vote_task(self, *args, **kwargs):
    logger.debug(kwargs)
    return "vote_task DONE"


@shared_task(bind=True)
def subscribe_task(self, *args, **kwargs):
    logger.debug(kwargs)
    return "subscribe_task DONE"


@shared_task(bind=True)
def comment_task(self, *args, **kwargs):
    logger.debug(kwargs)
    return "comment_task DONE"


@shared_task(bind=True)
def reaction_task(self, *args, **kwargs):
    logger.debug(kwargs)
    return "reaction_task DONE"
