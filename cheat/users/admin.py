from django.contrib import admin

from .models import CommentTask, CustomUser, SubscribeTask, ViewTask, VotingTask

admin.site.register(CustomUser)
admin.site.register(ViewTask)
admin.site.register(SubscribeTask)
admin.site.register(CommentTask)
admin.site.register(VotingTask)
