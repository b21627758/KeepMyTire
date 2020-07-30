import os
from django.contrib import messages
from django.views.generic import FormView
from rest_framework import generics
from django.http import HttpResponse
from django.views import View
from core.models import models
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from core.forms import register_form, login_form
from core import models
from django.utils import datetime_safe


# from user.serializers import UserSerializer, CustomerSerializer, StaffSerializer

class RegisterView(FormView):
    """Create a new user in the system"""
    # serializer_class = UserSerializer
    form_class = register_form.Register
    model = models.User
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})


class LoginView(View):
    """Login page view"""
    form_class = login_form.Login
    template_name = 'login_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = authenticate(request, email=form.email, password=form.password)
        if user is not None:
            user.last_login = datetime_safe.datetime.now()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})


class CreateCustomerView(View):
    """Create a new customer in the system"""
    # serializer_class = CustomerSerializer


class CreateStaffView(View):
    """Create a new staff in the system"""
    # serializer_class = StaffSerializer
