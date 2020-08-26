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
from core.forms import tire_form, tire_on_car_form
from core import models
from django.utils import datetime_safe


class CreateTireView(UserPassesTestMixin, View):
    """Create Tire"""
    form_class = tire_form.CreateTireForm
    model = models.Tire
    template_name = 'create_tire.html'

    def test_func(self):
        return self.request.user.is_staff

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Render create customer tire"""
        brands = ["Michelin",
                  "Pirelli",
                  "Hankook ",
                  "Goodyear",
                  "Kumho ",
                  "Lassa ",
                  "Petlas ",
                  "Starmaxx ",
                  "Nokian ",
                  "Bridgestone ",
                  "Continental ",
                  "Falken ",
                  "Kormoran ",
                  "Yokohama ",
                  "WindForce ",
                  "Nexen ",
                  "Dunlop ",
                  "Laufenn ",
                  "Milestone ",
                  "Marshal ",
                  "BFGoodrich ",
                  "Gt-Radial ",
                  "Sava ",
                  "Dayton ",
                  "Debica ",
                  "General ",
                  "Riken ",
                  "Roadstone",
                  "momo ",
                  "Tigar ",
                  "Farroad ",
                  "Semperit ",
                  "KLEBER ",
                  "Toyo ",
                  "Tracmax ",
                  "Rotalla ",
                  "Kinforest ",
                  "Saferich",
                  "Aplus ",
                  "Barum ",
                  "NANKANG ",
                  "Taurus ",
                  "Vitour ",
                  "General Tire",
                  "Kormetal ",
                  "Matador",
                  "Cratos",
                  "Fulda ",
                  "Maxxis",
                  "Syron",
                  "Formula",
                  "Linglong ",
                  "Waterfall ",
                  "Accelera ",
                  "Gislaved ",
                  "Viking ",
                  "Hifly ",
                  "Winrun ",
                  "Altenzo ",
                  "Atlas ",
                  "Carvonn",
                  "Orium ",
                  "Saetta ",
                  "Strial",
                  "Sunitrac",
                  "Wanlı ",
                  "Evergreen ",
                  "Forsage ",
                  "Goodride",
                  "Jinyu ",
                  "Marshall",
                  "Otani ",
                  "Tatko ",
                  "V-netik",
                  "Özka"]
        return render(request, self.template_name, {'brands': brands})

    @method_decorator(login_required)
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


class TireDetailView(View):
    """Detail And Condition Reports"""

    template_name = 'tire_detail.html'
    model = models.Tire

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        tire = self.model.objects.get(id=request.GET['pg'])
        crs = models.ConditionReport.objects.filter(tire_id=request.GET['pg'])
        return render(request, self.template_name, {'crs': crs, 'tire': tire})


class MoveTireView(View):
    """Move Tire To Vehicle"""

    template_name = 'move_tire.html'
    model = models.TireOnCar
    form_class = tire_on_car_form.TireOnCar

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        customer = request.GET.get('customer', None)
        cars = models.Car.objects.filter(owner_id=customer)
        tires_on_car = models.TireOnCar.objects.values_list('tire', flat=True)
        tires = models.Tire.objects.exclude(id__in=tires_on_car).filter(owner_id=customer)
        return render(request, self.template_name, {'cars': cars, 'customer': customer, 'tires': tires})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            car_id = models.Car.objects.get(plate=form.cleaned_data['car']).id
            tire = models.Tire.objects.get(id=form.cleaned_data['tire'])
            try:
                mtire = models.TireOnCar.objects.get(car_id=car_id, tire__position=tire.position)
            except self.model.DoesNotExist:
                self.model.objects.create(staff=request.user, tire_id=form.cleaned_data['tire'], car_id=car_id)
                return HttpResponse(status=200)
            mtire.delete()
            self.model.objects.create(staff=request.user, tire_id=form.cleaned_data['tire'], car_id=car_id)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
