from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
        return f"{self.email} #{self.id}"


class TaskMixin(models.Model):
    channel = models.CharField("Канал", max_length=120)
    amount = models.IntegerField("Объем", default=0)
    processed_count = models.IntegerField("Выполненный объем", default=0)
    price = models.IntegerField("Стоимость", default=0)
    duration = models.IntegerField("Подписка(дней)", default=0)
    task_duration = models.IntegerField("Продолжительность услуги(минут)")
    subscription = models.BooleanField("Подписка", default=False)
    max_speed = models.BooleanField("Максимальная скорость", default=False)
    viewed = models.BooleanField("Просмотрен", default=False)
    processed = models.BooleanField("Обработан", default=False)
    begin_time = models.DateTimeField("Время начала", default=timezone.now)
    update_time = models.DateTimeField("Время обновления", auto_now=True)
    creation_time = models.DateTimeField("Время создания", auto_now_add=True)

    def get_processed_percent(self):
        if self.amount:
            return float(self.processed_count) / self.amount * 100

    @property
    def class_name(self):
        names = {
            "ViewTask": "Просмотры",
            "CommentTask": "Комментарии",
            "SubscribeTask": "Подписка",
            "VotingTask": "Голосование",
            "ReactionTask": "Реакции",
        }
        name = self.__class__.__name__
        return names.get(name, "Задача")


class ViewTask(TaskMixin):
    """Задача: просмотр публикации"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    count_last_posts = models.IntegerField("Кол-во последних постов", default=0)
    count_per_post = models.IntegerField("Объем на пост", default=False)
    count_avg = models.IntegerField("Среднее кол-во постов в день", default=False)

    def __str__(self) -> str:
        return str(f"Задача: #{self.id} Клиент: {self.user.email}")

    class Meta:
        db_table = "view_task"


class SubscribeTask(TaskMixin):
    """Задача: подписка на канал"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sub_type = models.BooleanField("Вариант подписки", default=True)
    read_last_post = models.BooleanField("Чтение последних постов", default=False)
    gender_choice = models.CharField(choices=GENDERS, max_length=120)

    def __str__(self) -> str:
        return str(f"Задача: #{self.id} Клиент: {self.user.email}")

    class Meta:
        db_table = "sub_task"


class CommentTask(TaskMixin):
    """Задача: Оставить комментарий"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comments = models.JSONField(null=True)

    def __str__(self) -> str:
        return str(f"Задача: #{self.id} Клиент: {self.user.email}")

    class Meta:
        db_table = "comment_task"


class VotingTask(TaskMixin):
    """Задача: голосование"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    scatter = models.BooleanField("Разброс +- 5%", default=False)
    post_id = models.IntegerField("Номер поста", null=True, blank=True)
    posts = models.JSONField(null=True)

    def __str__(self) -> str:
        return str(f"Задача: #{self.id} Клиент: {self.user.email}")

    class Meta:
        db_table = "voting_task"
