from celery import shared_task
from django.db.models import F
from loguru import logger
from session.models import Session
from tasks.models import (CommentTask, ReactionTask, SubscribeTask, ViewTask,
                          VotingTask)

from .service.telegram_func import SubscribeTaskObject, ViewTaskObject

# celery -A config.celery worker --loglevel=INFO
# celery -A config.celery beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A config worker --loglevel=info

# FLOWER celery -A config flower --port=5554
# DRAMATIQ


@shared_task(bind=True)
def views_task(self, *args, **kwargs):
    logger.debug(kwargs)
    session_dict = Session.objects.filter(name="+79640372969").values('app_id', 'app_hash', "auth_string")
    logger.debug(session_dict[0])
    
    session_ = {'app_id': session_dict[0]['app_id'], 
                'app_hash': str(session_dict[0]['app_hash']),
                'auth_string': str(session_dict[0]['auth_string'])}
    views_task = ViewTaskObject(session_data=session_, 
                                group_url=kwargs['channel'], 
                                count_last_posts=kwargs['count_last_posts'],
                                count_per_post=kwargs['count_per_post'],
                                post_id=kwargs['post_id'])
    
    tasks_status = views_task.increase_post_views_count()
    return "done"


@shared_task(bind=True)
def vote_task(self, *args, **kwargs):
    logger.debug(kwargs)
    return "vote_task DONE"


@shared_task(bind=True)
def subscribe_task(self, *args, **kwargs):
    sub_per_hour = int(int(kwargs['amount'])/int(kwargs['task_duration']))
    logger.debug(f"Всего подписчиков в минуту: {sub_per_hour}")
    
    session_dict = Session.objects.filter(name="+79640372969").values('app_id', 'app_hash', "auth_string")
    
    
    session_ = {'app_id': session_dict[0]['app_id'], 
                'app_hash': str(session_dict[0]['app_hash']),
                'auth_string': str(session_dict[0]['auth_string'])}
    sub_task = SubscribeTaskObject(session_data=session_, 
                                group_url=kwargs['channel'], 
                               )
    
    tasks_status = sub_task.subscribe_to_channel()
    if tasks_status:
        SubscribeTask.objects.filter(id=kwargs['task_id']).update(processed_count=F('processed_count')+1)
    
    return "done"


@shared_task(bind=True)
def comment_task(self, *args, **kwargs):
    logger.debug(kwargs)
    return "comment_task DONE"


@shared_task(bind=True)
def reaction_task(self, *args, **kwargs):
    logger.debug(kwargs)
    return "reaction_task DONE"
