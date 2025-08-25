from django.urls import path
from .views import show_all_users

urlpatterns = [
    path('all_users', show_all_users, name='show_all_users'),
]