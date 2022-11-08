from django.contrib import admin

from .models import Channel, Session

admin.site.register(Session)
admin.site.register(Channel)