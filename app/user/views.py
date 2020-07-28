import os

from django.views.generic import FormView
from rest_framework import generics
from django.http import HttpResponse
from django.views import View
from core.models import models
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from core.forms import register_form
from core import models


# from user.serializers import UserSerializer, CustomerSerializer, StaffSerializer

class RegisterView(FormView):
    """Create a new user in the system"""
    # serializer_class = UserSerializer
    form_class = register_form
    model = models.User
    template_name = 'register_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        comein = request.POST
        new_user = models.User()
        new_user.email = comein.get('email')
        new_user.first_name = comein.get('first_name')
        new_user.last_name = comein.get('last_name')
        new_user.phone_num = comein.get('phone_num')
        new_user.date_of_birth = comein.get('date_of_birth')
        new_user.save()
        return redirect('index')



class CreateCustomerView(View):
    """Create a new customer in the system"""
    # serializer_class = CustomerSerializer


class CreateStaffView(View):
    """Create a new staff in the system"""
    # serializer_class = StaffSerializer
