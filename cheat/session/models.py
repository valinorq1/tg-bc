from django.db import models


# Create your models here.
class Session(models.Model):
    name = models.CharField("Имя сессии", max_length=120)
    app_id = models.IntegerField("app_id", null=False)
    app_hash = models.CharField("app_hash", null=False, max_length=128)
    updated_at = models.DateTimeField("Время обновления", auto_now=True)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "session"
