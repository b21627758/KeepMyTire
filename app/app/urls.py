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
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('user/', include('user.urls')),
    path('create-customer/', user_views.CreateCustomerView.as_view(), name='create-customer'),
    path('create-staff/', user_views.CreateStaffView.as_view(), name='create-staff'),
    path('list-customer/', user_views.ListCustomerView.as_view(), name='list-customer'),
    path('', views.index, name='index'),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('logout/', user_views.LogOutView.as_view(), name='logout'),
    path('register/', user_views.RegisterView.as_view(), name='register'),
]
