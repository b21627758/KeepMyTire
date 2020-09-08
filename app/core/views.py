from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render
from django.contrib.auth import get_user_model


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")
