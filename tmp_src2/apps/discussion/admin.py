from django.contrib import admin
from .models import Discussion, DiscussionReply, Vote

admin.site.register(Discussion)
admin.site.register(DiscussionReply)
admin.site.register(Vote)
