from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('create-customer/', views.CreateCustomerView.as_view(), name='create-customer'),
    path('create-staff/', views.CreateStaffView.as_view(), name='create-staff'),
]
