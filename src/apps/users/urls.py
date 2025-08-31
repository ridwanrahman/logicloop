from django.urls import path
from .views import show_all_users, example_view

urlpatterns = [
    path('all_users', show_all_users, name='show_all_users'),
    path('example', example_view, name='example_view')
]