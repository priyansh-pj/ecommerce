from django.urls import path
from .views import *
from django.shortcuts import render


def home(request):
    return render(request, 'template.html')


urlpatterns = [
    path("", home, name="home")
]
