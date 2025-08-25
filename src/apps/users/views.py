from django.shortcuts import render

from .models import User

# Create your views here.
def show_all_users(request):
    users = User.objects.all()
    users_dict = {
        "users": users
    }
    return render(request, "pages/all-users.html", users_dict)