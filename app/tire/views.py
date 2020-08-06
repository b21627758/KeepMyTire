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
    """Create Tire"""
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
            tire = form.save(commit=False)
            customer_id = request.GET['pg']
            tire.owner = get_user_model().objects.get(id=customer_id)
            tire.save()
            return redirect(f'/list-customer-tires/?pg={customer_id}')
        else:
            return render(request, self.template_name, {'form': form})


class ListTireView(UserPassesTestMixin, View):
    """List Tires of customer"""

    template_name = 'list_tire.html'

    def test_func(self):
        return self.request.user.is_staff

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        tires = models.Tire.objects.filter(owner_id=request.GET['pg'])
        return render(request, self.template_name, {'context': tires})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            tire = models.Tire.objects.get(id=request.POST.get('Tid', None))
            tire.delete()
        except models.Tire.DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, self.template_name)
        messages.success(request, "The user is deleted")
        return render(request, self.template_name, {'context': models.Tire.objects.filter(owner_id=request.GET['pg'])})
