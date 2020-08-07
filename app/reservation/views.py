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
from core.forms import reservation_form
from core import models
from django.utils import datetime_safe


class MakeReservationView(View):
    """Create Reservation View"""

    form_class = reservation_form.BookingForm
    model = models.Reservation
    template_name = 'make_reservation.html'

    def get(self, requests, *args, **kwargs):
        return render(requests, self.template_name)
