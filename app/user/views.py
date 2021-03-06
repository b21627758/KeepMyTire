import os
from datetime import date, datetime, time

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
from core.forms import register_form, login_form, customer_form, reservation_form
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
        try:
            if form.is_valid():
                try:
                    user = get_user_model().objects.get(email=form.cleaned_data['email'])
                except get_user_model().DoesNotExist:
                    form.save()
                    return redirect('index')
                user.set_password(form.cleaned_data['password1'])
                user.is_active = True
                user.date_of_birth = form.cleaned_data['date_of_birth']
                user.save()
                return redirect('index')
            else:
                return render(request, self.template_name, {'form': form})
        except ValueError:
            form.add_error('email', 'Email Already Exists')
            return render(request, self.template_name, {'form': form})


class LoginView(View):
    """Login page view"""
    form_class = login_form.Login
    template_name = 'login_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = EmailBackend.authenticate(request, username=form.cleaned_data['email'],
                                             password=form.cleaned_data['password'])
            if user is not None:
                user.last_login = datetime_safe.datetime.now()
                user.save()
                login(request, user)
                return redirect('index')
            else:
                form.add_error('email', 'Not Valid Email Or Password')
                return render(request, self.template_name, {'form': form})
        else:
            form.add_error('email', 'Not Valid Email Or Password')
            return render(request, self.template_name, {'form': form})


class LogOutView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


class CreateCustomerView(UserPassesTestMixin, View):
    """Create a new customer in the system"""
    form_class = customer_form.CreateCustomerForm
    template_name = 'create_customer_form.html'

    def test_func(self):
        return self.request.user.is_staff

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                user = get_user_model().objects.get(email=form.cleaned_data['email'])
            except get_user_model().DoesNotExist:
                form.save()
                user = get_user_model().objects.get(email=form.cleaned_data['email'])
                user.is_active = False
                user.save()
                return redirect('list-customer')
            return render(request, self.template_name, {'form': form})

        else:
            return render(request, self.template_name, {'form': form})


class CreateStaffView(UserPassesTestMixin, View):
    """Create a new staff in the system"""
    # serializer_class = StaffSerializer
    form_class = customer_form.CreateCustomerForm
    template_name = 'create_customer_form.html'

    def test_func(self):
        return self.request.user.is_superuser

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Display create staff"""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = get_user_model().objects.get(email=form.cleaned_data['email'])
            user.is_active = False
            user.is_staff = True
            user.save()
            return redirect('list-staff')
        return render(request, self.template_name, {'form': form})


class ListStaffView(View):
    """List existing staff"""

    template_name = 'list_customer.html'

    def test_func(self):
        return self.request.user.is_superuser

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        customers = get_user_model().objects.filter(is_staff=True, is_superuser=False)
        return render(request, self.template_name, {'context': customers})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(email=request.POST.get('context', None))
            user.delete()
        except get_user_model().DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, self.template_name)
        messages.success(request, "The user is deleted")
        return render(request, self.template_name, {})


class ListCustomerView(UserPassesTestMixin, View):
    """List existing customers"""

    template_name = 'list_customer.html'

    def test_func(self):
        return self.request.user.is_staff

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        customers = get_user_model().objects.filter(is_staff=False)
        return render(request, self.template_name, {'context': customers})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(email=request.POST.get('context', None))
            user.delete()
        except get_user_model().DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, self.template_name)
        messages.success(request, "The user is deleted")
        return render(request, self.template_name, {})


class CustomerDetailView(UserPassesTestMixin, View):
    """Detailed Customer"""

    template_name = 'customer_detail_page.html'

    def test_func(self):
        return self.request.user.is_staff

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id=request.GET['pg'])
        return render(request, self.template_name, {'customer': user})


class ProfileView(View):
    """User Profile Page"""

    template_name = 'profile.html'

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {})


class StaffReservationView(View):
    """Show reserved days and process"""

    template_name = 'show_reservation.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Show waiting reservations"""
        reservations = models.Reservation.objects.filter(staff=request.user, status=0)
        for i in reservations:
            if i.date < datetime.today().date() or (i.date == datetime.today() and i.time < datetime.now().time()):
                i.status = 3
                i.save()
                reservations.exclude(i)
        return render(request, self.template_name, {'reservations': reservations})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Convert reservation to done"""
        reservation = models.Reservation.objects.get(id=request.POST.get('reservation', None))
        reservation.status = 1
        reservation.save()
        return render(request, self.template_name)


class CustomerOwnedTireView(View):
    """Show owned tires"""

    template_name = 'list_tire.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        tires = models.Tire.objects.filter(owner=request.user)
        if tires.exists():
            return render(request, self.template_name, {'context': tires})
        else:
            return render(request, self.template_name, {'failure': True})


class CustomerReservationView(View):
    """Show reserved days and process"""

    template_name = 'show_reservation.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Show reservations"""
        reservations = models.Reservation.objects.filter(customer=request.user).order_by('status')
        for i in reservations:
            if i.date < date.today() and i.status == 0:
                i.status = 3
            elif i.date == datetime.now().date() and i.time < datetime.now().time() and i.status == 0:
                i.status = 3
            i.save()
        return render(request, self.template_name, {'reservations': reservations})


class CustomerOwnedCarView(View):
    """Show owned cars"""

    template_name = 'list_cars.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """List cars"""
        cars = models.Car.objects.filter(owner=request.user)
        tires = {}
        if cars.exists():
            for i in cars:
                tires[int(i.id)] = []
                for j in models.TireOnCar.objects.filter(car_id=i.id):
                    tires[int(i.id)].append(models.Tire.objects.get(id=j.tire.id))
            return render(request, self.template_name, {'context': cars, 'tires': tires})
        else:
            return render(request, self.template_name, {'failure': True})
