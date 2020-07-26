from rest_framework import generics
from user.serializers import UserSerializer, CustomerSerializer, StaffSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateCustomerView(generics.CreateAPIView):
    """Create a new customer in the system"""
    serializer_class = CustomerSerializer


class CreateStaffView(generics.CreateAPIView):
    """Create a new staff in the system"""
    serializer_class = StaffSerializer
