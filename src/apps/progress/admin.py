from django.contrib import admin
from .models import UserProgress, Achievement, UserAchievement

admin.site.register(UserProgress)
admin.site.register(Achievement)
admin.site.register(UserAchievement)