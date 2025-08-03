from django.http import HttpResponse
from django.shortcuts import render


def health_check(request):
    """
    Health check endpoint to verify API is running
    """
    return HttpResponse("Application is running", content_type="text/plain")

def show_homepage(request):
    """
    Show the homepage
    """
    return render(request, 'pages/hello-world.html', {})
