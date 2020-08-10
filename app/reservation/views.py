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
from core.models import Reservation
from datetime import date, timedelta


def get_customer(request):
    reservation = Reservation.objects.filter(staff__email=request.GET.get('context', None),
                                             date__gte=date.today(),
                                             date__lte=date.today() + timedelta(days=7)).values('date')
    return render(request, 'make_reservation.html', {'disabled_dates': reservation})


class MakeReservationView(View):
    """Create Reservation View"""

    form_class = reservation_form.BookingForm
    model = Reservation
    template_name = 'make_reservation.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        staffs = get_user_model().objects.filter(is_staff=True,
                                                 is_superuser=False)  # first get staff then select reservation to this staff
        records = {}
        for staff in staffs:
            record = Reservation.objects.filter(date__lte=date.today() + timedelta(days=7), date__gte=date.today(),
                                                staff=staff).values('date')
            records[str(staff.email)] = record
        return render(request, self.template_name, {'disabled_dates': records})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if Reservation.objects.filter(date=form.cleaned_data['date']).exists():
                for i in Reservation.objects.filter(date=form.cleaned_data['date']):
                    if i.time == form.cleaned_data['time']:
                        return render(request, self.template_name, {'error': 'Selected Day-Time is Full',
                                                                    'focus_date': form.cleaned_data['date'],
                                                                    'focus_time': form.cleaned_data['time']})
            reservation = form.save(commit=False)
            reservation.customer = request.user
            reservation.status = 0
            reservation.staff = get_user_model().objects.get(email=form.cleaned_data['staff'])
            reservation.save()
            return render(request, self.template_name, {'form': form, 'success': 'true'})
        return render(request, self.template_name, {'form': form, 'success': ''})
