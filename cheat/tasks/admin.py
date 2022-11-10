from django.contrib import admin

from .models import (CommentTask, ReactionTask, SubscribeTask, ViewTask,
                     VotingTask)

admin.site.register(ViewTask)
admin.site.register(SubscribeTask)
admin.site.register(CommentTask)
admin.site.register(VotingTask)
admin.site.register(ReactionTask)
