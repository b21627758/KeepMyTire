from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone_num')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create user with registration"""

        print("TEST")

        if get_user_model().objects.filter(email=validated_data['email']).exists():
            return get_user_model().objects.patch(**validated_data)
        return get_user_model().objects.register(**validated_data)

    def update(self, instance, validated_data):
        """Update a user"""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CustomerSerializer(UserSerializer):
    """Serializer for the customer"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_num')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create for customer"""
        return get_user_model().objects.create_customer(**validated_data)


class StaffSerializer(UserSerializer):
    """Serializer for the staff"""

    def create(self, validated_data):
        """Create for staff"""
        return get_user_model().objects.create_staff(**validated_data)
