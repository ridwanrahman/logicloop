from django.http import HttpResponse
from django.shortcuts import render


def health_check(request):
    return HttpResponse("OK")


def show_homepage(request):
    return render(request, "pages/hello-world.html", {})