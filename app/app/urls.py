"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from car import views as car_views
from tire import views as tire_views
from user import views as user_views
from reservation import views as res_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('create-customer/', user_views.CreateCustomerView.as_view(), name='create-customer'),
    path('create-staff/', user_views.CreateStaffView.as_view(), name='create-staff'),
    path('list-customer/', user_views.ListCustomerView.as_view(), name='list-customer'),
    path('customer-detail/', user_views.CustomerDetailView.as_view(), name='customer-detail'),
    path('list-customer-tires/', tire_views.ListTireView.as_view(), name='list-customer-tires'),
    path('create-tire/', tire_views.CreateTireView.as_view(), name='create-tire'),
    path('', views.index, name='index'),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    path('create-staff/', user_views.CreateStaffView.as_view(), name='create-staff'),
    path('list-staff/', user_views.ListStaffView.as_view(), name='list-staff'),
    path('logout/', user_views.LogOutView.as_view(), name='logout'),
    path('register/', user_views.RegisterView.as_view(), name='register'),
    path('make-reservation/', res_views.MakeReservationView.as_view(), name='make-reservation'),
    path('show-rez/', user_views.StaffReservationView.as_view(), name='show-rez'),
    path('list-my-tires/', user_views.CustomerOwnedTireView.as_view(), name='list-my-tires'),
    path('list-my-rez/', user_views.CustomerReservationView.as_view(), name='list-my-rez'),
    path('list-my-cars', user_views.CustomerOwnedCarView.as_view(), name='list-my-cars'),
    path('get-cus/', res_views.get_customer, name='get-custom'),
    path('add-car/', car_views.CreateCustomerCarView.as_view(), name='add-car'),
    path('list-car/', car_views.CustomerCarListView.as_view(), name='list-cars'),
    path('cond-rep/', res_views.ConditionReportView.as_view(), name='cond-rep'),
    path('tire-detail/', tire_views.TireDetailView.as_view(), name='tire-detail'),
    path('last-report/', res_views.LastReportView.as_view(), name='last-report'),
    path('cs-show/', res_views.ConditionReportShowView.as_view(), name='cs-show'),
    path('cs-detail/', res_views.ConditionReportDetailView.as_view(), name='cs-detail'),
    path('mt/', tire_views.MoveTireView.as_view(), name='mt')
]
