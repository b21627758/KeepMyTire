import uuid
import os

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from phone_field import PhoneField
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and save new user, password None equals Non-active user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Create and save superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user

    def register(self, email, password):
        """Register only create active user with mandatory password"""
        if not password:
            raise ValueError
        user = self.create_user(email, password)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    F_name = models.CharField(max_length=255)
    L_name = models.CharField(max_length=255)
    DoB = models.DateField()
    P_num = PhoneField(blank=True, help_text='Contact Phone Number')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
