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
from core.forms import customer_car_add_form
from core import models
from django.utils import datetime_safe


class CreateCustomerCarView(View):
    """Create Car for customer view"""

    form_class = customer_car_add_form.CreateCarForm
    model = models.Car
    template_name = 'add_customer_car.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            owner = request.GET['pg']
            car.owner = get_user_model().objects.get(id=owner)
            car.plate = form.cleaned_data['plate']
            car.save()
            return redirect(f'/list-car/?pg={owner}')
        return render(request, self.template_name, {'Failure': True})


class CustomerCarListView(View):
    """List Cars"""

    template_name = 'list_cars.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        cars = models.Car.objects.filter(owner__id=request.GET['pg'])
        tires = {}
        for i in cars:
            tires[int(i.id)] = []
            for j in models.TireOnCar.objects.filter(car_id=i.id):
                tires[int(i.id)].append(models.Tire.objects.get(id=j.tire.id))
        return render(request, self.template_name, {'context': cars, 'tires': tires})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            car = models.Car.objects.get(plate=request.POST.get('context', None))
            car.delete()
        except models.Car.DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, self.template_name)
        messages.success(request, "The user is deleted")
        return render(request, self.template_name, {})
