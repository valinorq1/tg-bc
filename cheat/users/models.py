from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from loguru import logger

from users.service.model_utils import create_task_schedule

from .managers import CustomUserManager

GENDERS = [
    ("A", "Случайно"),
    ("M", "Мужской"),
    ("F", "Женский"),
]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    balance = models.IntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} #{self.pk}"


class TransactionHistory(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="transactions"
    )
    creation_time = models.DateTimeField("Время создания", auto_now_add=True)
    total_sum = models.IntegerField(null=False)

    def __str__(self) -> str:
        return f"{self.user.email} {self.total_sum}"

    class Meta:
        db_table = "transaction_history"


class TaskMixin(models.Model):
    channel = models.CharField("Канал", max_length=120)
    post_id = models.IntegerField(null=False)
    amount = models.IntegerField("Объем", default=0)
    processed_count = models.IntegerField("Выполненный объем", default=0)
    price = models.IntegerField("Стоимость", default=0)
    duration = models.IntegerField("Подписка(дней)", default=0)
    task_duration = models.IntegerField("Продолжительность услуги(минут)")
    subscription = models.BooleanField("Подписка", default=False)
    max_speed = models.BooleanField("Максимальная скорость", default=False)
    viewed = models.BooleanField("Просмотрен", default=False)
    processed = models.BooleanField("Обработан", default=False)
    begin_time = models.DateTimeField("Время начала", null=True, blank=True)
    update_time = models.DateTimeField("Время обновления", auto_now=True)
    creation_time = models.DateTimeField("Время создания", auto_now_add=True)

    def get_processed_percent(self):
        if self.amount:
            return float(self.processed_count) / self.amount * 100

    class Meta:
        abstract = True


class ViewTask(TaskMixin):
    """Задача: просмотр публикации"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    count_last_posts = models.IntegerField("Кол-во последних постов", default=0)
    count_per_post = models.IntegerField("Объем на пост", default=False)
    count_avg = models.IntegerField("Среднее кол-во постов в день", default=False)

    def __str__(self) -> str:
        return str(f"Задача: #{self.pk} Клиент: {self.user.email}")

    class Meta:
        db_table = "view_task"


@receiver(post_save, sender=ViewTask)
def create_view_task_schedule(sender, instance, **kwargs):
    """view task task schedule creator"""
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

    created = create_task_schedule(
        name=f"Просмотры: {task_name}",
        start_time=start_at,
        arguments=args_for_sched,
        celery_task_name="views_task",
    )


class SubscribeTask(TaskMixin):
    """Задача: подписка на канал"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sub_type = models.BooleanField("Вариант подписки", default=True)
    read_last_post = models.BooleanField("Чтение последних постов", default=False)
    gender_choice = models.CharField(choices=GENDERS, max_length=120)

    def __str__(self) -> str:
        return str(f"Задача: #{self.pk} Клиент: {self.user.email}")

    class Meta:
        db_table = "sub_task"


@receiver(post_save, sender=SubscribeTask)
def create_subscribe_task_schedule(sender, instance, **kwargs):
    """sybscrube task schedule creator"""
    logger.debug(instance.gender_choice)
    duration = False
    if instance.max_speed:
        duration = True
    args_for_sched = {
        "task_id": instance.id,
        "amount": instance.amount,
        "channel": instance.channel,
        "max_speed": instance.max_speed,
        "task_duration": duration,
        "read_last_post": instance.read_last_post,
        "gender": instance.gender_choice,
        "sub_type": instance.sub_type,
    }

    task_name = str(instance).replace("Задача:", "")
    start_at = datetime.now() + timedelta(seconds=10)

    if instance.begin_time:
        start_at = instance.begin_time
    created = create_task_schedule(
        name=f"Подписка: {task_name}",
        start_time=start_at,
        arguments=args_for_sched,
        celery_task_name="subscribe_task",
    )


class CommentTask(TaskMixin):
    """Задача: Оставить комментарий"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comments = models.JSONField(null=True)

    def __str__(self) -> str:
        return str(f"Задача: #{self.pk} Клиент: {self.user.email}")

    class Meta:
        db_table = "comment_task"


@receiver(post_save, sender=CommentTask)
def create_comment_task_schedule(sender, instance, **kwargs):
    """comment task schedule creator"""
    args_for_sched = {
        "task_id": instance.id,
        "channel": instance.channel,
        "post_id": instance.post_id,
        "comment_list": instance.comments,
    }

    task_name = str(instance).replace("Задача:", "")
    start_at = datetime.now() + timedelta(seconds=10)

    if instance.begin_time:
        start_at = instance.begin_time
    created = create_task_schedule(
        name=f"Комментарии: {task_name}",
        start_time=start_at,
        arguments=args_for_sched,
        celery_task_name="comment_task",
    )


class VotingTask(TaskMixin):
    """Задача: голосование"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    scatter = models.BooleanField("Разброс +- 5%", default=False)
    post_id = models.IntegerField("Номер поста", null=True, blank=True)
    posts = models.JSONField(null=True)

    def __str__(self) -> str:
        return str(f"Задача: #{self.pk} Клиент: {self.user.email}")

    class Meta:
        db_table = "voting_task"


class Reaction(models.Model):
    name = models.CharField("Эмоция", unique=True, max_length=32)
    premium = models.BooleanField("Премиум", default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "reactions"


class ReactionTask(TaskMixin):
    """Задача: оставить реакцию на  пост"""

    new_posts_count = models.IntegerField(
        "Количесвто новых постов", null=True, blank=True
    )
    scatter = models.BooleanField("Разброс +- 5%", default=False)
    post = models.CharField("Ссылка на пост", max_length=120)
    # reactions = models.ManyToManyField(Reaction, null=True, blank=True)
    emotion = models.JSONField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = "reactions_task"
