from django.db import models
from django.utils import timezone


class Channel(models.Model):
    channel = models.CharField(max_length=128)
    creation_time = models.DateTimeField("Время создания", auto_now_add=True)
    
    def __str__(self):
        return self.channel
    
    class Meta:
        db_table = "channel_list"
    
    
class Session(models.Model):
    name = models.CharField("Имя сессии", max_length=120)
    app_id = models.IntegerField("app_id", null=False)
    app_hash = models.CharField("app_hash", null=False, max_length=128)
    auth_string = models.CharField("auth_string", null=False, max_length=1024)
    updated_at = models.DateTimeField("Время обновления", auto_now=True)
    last_action = models.DateTimeField("Последнее действие", default=timezone.now)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    is_busy = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    banned_until = models.DateTimeField(null=True, blank=True)
    
    subscribed_to = models.ManyToManyField(Channel, related_name="sub_to",  blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "session"


""" class SubsribeUntil(models.Model):
    channel = models.ForeignKey(Channel, related_name="sub_until", on_delete=models.CASCADE)
    sub_until = models.DateTimeField(blank=True, null=True)
    session =  """

class ViewTaskInfo(models.Model):
    """История просмотров какая сессиия какой пост смотрела"""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="view_task_info")
    channel = models.CharField(null=False, max_length=128)
    post_id = models.IntegerField(null=False)
    
    def __str__(self) -> str:
        return f"{self.session.name} {self.channel}/{self.post_id}"
    
    class Meta:
        db_table = "view_task_logs"
    
