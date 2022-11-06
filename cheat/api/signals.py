import json
from datetime import datetime, timedelta

from dateutil import parser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from loguru import logger
from users.models import ViewTask


@receiver(post_save, sender=ViewTask)
def create_view_task_schedule(sender, instance, **kwargs):
    args_for_sched = {
        "task_id": instance.id,
        "amount": instance.amount,
        "channel": instance.channel,
        "max_speed": instance.max_speed,
        "sub_duration": instance.duration if instance.duration else 0,
        "subscription": True if instance.subscription else False,
        "count_last_posts": instance.count_last_posts,
        "count_per_post": instance.count_per_post,
    }

    task_name = str(instance).replace("Задача:", "")
    start_at = datetime.now() + timedelta(seconds=10)

    if instance.begin_time:
        start_at = instance.begin_time

    clocked = ClockedSchedule.objects.create(clocked_time=start_at)

    new_celery_task = PeriodicTask.objects.update_or_create(
        name=f"Просмотры: {task_name}",
        defaults={
            "task": "api.tasks.reaction_task",
            "kwargs": json.dumps(args_for_sched),
            "one_off": True,
            "clocked": clocked,
        },
    )
