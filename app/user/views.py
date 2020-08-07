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
from core.forms import register_form, login_form, customer_form
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


class MakeReservationSelfView(View):
    """Make Tire Change Reservation"""

    template_name = 'make_reservation.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        pass


class MakeReservationToCustomer(View):
    """Make Tire Change Reservation For Customer"""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        pass
