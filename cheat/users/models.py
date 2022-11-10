from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from loguru import logger

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    balance = models.IntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    
    def get_user_base_data(self):
        return f"{self.email} {self.balance}"

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