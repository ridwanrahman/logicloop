from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


PROJECT_NAME=getattr(settings, "PROJECT_NAME")

def health_check(request):
    """
    Health check endpoint to verify API is running
    """
    return HttpResponse("Application is running", content_type="text/plain")

def show_homepage(request):
    """
    Show the homepage
    """
    return render(request, 'pages/hello-world.html', {"project_name": PROJECT_NAME})
