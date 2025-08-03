from django.http import HttpResponse


def health_check(request):
    """
    Health check endpoint to verify API is running
    """
    return HttpResponse("Application is running", content_type="text/plain")