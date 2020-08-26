import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from rest_framework import generics
from django.http import HttpResponse
from django.views import View
from rest_framework.utils import json
from django.core import serializers
from core.models import Tire
from django.contrib.auth import get_user_model, authenticate, login, logout
from core.backends import EmailBackend
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from core.forms import reservation_form, condition_report_form
from core.models import Reservation, ConditionReport, Tire
from datetime import date, timedelta, datetime


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

        return render(request, self.template_name, {'staffs': staffs})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            staffs = get_user_model().objects.filter(is_staff=True,
                                                     is_superuser=False)  # first get staff then select reservation to this staff
            if Reservation.objects.filter(date=form.cleaned_data['date'],
                                          staff__email=form.cleaned_data['staff']).exists():
                for i in Reservation.objects.filter(date=form.cleaned_data['date'],
                                                    staff__email=form.cleaned_data['staff']):
                    if i.time == form.cleaned_data['time']:
                        return render(request, self.template_name, {'error': 'Selected Day-Time is Full',
                                                                    'focus_date': form.cleaned_data['date'],
                                                                    'focus_time': form.cleaned_data['time'],
                                                                    'staffs': staffs})
            elif form.cleaned_data['date'] < datetime.today().date():
                return render(request, self.template_name, {'error': 'Out of work time',
                                                            'focus_date': form.cleaned_data['date'],
                                                            'focus_time': form.cleaned_data['time'],
                                                            'staffs': staffs})
            elif form.cleaned_data['date'] == datetime.today().date():
                if form.cleaned_data['time'] <= datetime.now().time():
                    return render(request, self.template_name, {'error': 'Selected Time Passed',
                                                                'focus_date': form.cleaned_data['date'],
                                                                'focus_time': form.cleaned_data['time'],
                                                                'staffs': staffs})
            else:
                reservation = form.save(commit=False)
                reservation.customer = request.user
                reservation.status = 0
                reservation.staff = get_user_model().objects.get(email=form.cleaned_data['staff'])
                reservation.save()
                return redirect('list-my-rez')
        return render(request, self.template_name, {'form': form, 'success': ''})


class ConditionReportView(View):
    """Condition Report View"""

    template_name = 'condition_report.html'
    form_class = condition_report_form.CreateConditionReportForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Send Condition Report Form"""
        rez = Reservation.objects.get(id=request.GET.get('context', None))
        customer = rez.customer
        tires = Tire.objects.filter(owner_id=rez.customer_id)
        move = False
        if rez.process == 0 or rez.process == 1:
            move = True
        return render(request, self.template_name, {'tires': tires, 'move': move, 'customer': customer.id})

    def post(self, request, *args, **kwargs):
        """Keep Condition Reports"""
        form = self.form_class(request.POST)
        if form.is_valid():
            cr = form.save(commit=False)
            cr.reporter = request.user
            cr.date = datetime.today()
            cr.time = datetime.now().time()
            cr.save()
            return redirect('show-rez')
        return render(request, self.template_name, {'form': form})


class LastReportView(View):
    """Send Last Condition Report"""

    template_name = 'condition_report_show_one.html'
    model = ConditionReport

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        condition_report = self.model.objects.filter(tire_id=request.GET['pg']).order_by('-date').first()
        try:
            rp = get_user_model().objects.get(id=condition_report.reporter.id)
        except:
            return render(request, self.template_name, {'failure': True})
        return render(request, self.template_name, {'cr': condition_report, 'rp': rp})


class ConditionReportShowView(View):
    """Send report according to tire"""

    template_name = 'condition_report_list.html'
    model = ConditionReport

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        condition_report = self.model.objects.filter(tire_id=request.GET['pg']).order_by('date', 'time')
        return render(request, self.template_name, {'context': condition_report})


class ConditionReportDetailView(View):
    """Detailed Condition Report View"""

    model = ConditionReport
    template_name = 'condition_report_detail.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        cr = self.model.objects.get(id=request.GET['pg'])
        return render(request, self.template_name, {'cr': cr})
