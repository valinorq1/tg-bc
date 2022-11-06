from django.db import models


class Session(models.Model):
    name = models.CharField("Имя сессии", max_length=120)
    app_id = models.IntegerField("app_id", null=False)
    app_hash = models.CharField("app_hash", null=False, max_length=128)
    auth_string = models.CharField("auth_string", null=False, max_length=256)
    updated_at = models.DateTimeField("Время обновления", auto_now=True)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    is_busy = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    banned_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "session"
