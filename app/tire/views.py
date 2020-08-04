import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from rest_framework import generics
from django.http import HttpResponse
from django.views import View
from core.models import models
from django.contrib.auth import get_user_model, authenticate, login, logout
from core.backends import EmailBackend
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from core.forms import tire_form
from core import models
from django.utils import datetime_safe


class CreateTireView(UserPassesTestMixin, View):
    form_class = tire_form.CreateTireForm
    model = models.Tire
    template_name = 'create_tire.html'

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        """Render create customer tire"""
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """Create tire record for existing tire """
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-tire')
        else:
            return render(request, self.template_name, {'form': form})
