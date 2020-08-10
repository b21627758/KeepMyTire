import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and save new user, password None equals Non-active user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra):
        """Create and save superuser"""
        user = self.create_user(email, password, **extra)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    """Custom user model that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_num = models.CharField(max_length=11, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Car(models.Model):
    """Car model"""
    plate = models.CharField(max_length=10, unique=True)
    brand = models.CharField(max_length=100)
    color = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Tire(models.Model):
    """Tire model"""
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100)
    size = models.IntegerField()  # size types 14-22--> 0,1,2,3,4,5,6,7,8
    usage = models.IntegerField()  # summer-winter-snow-multipurpose--> 0,1,2,3
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class TireOnCar(models.Model):
    """Intermediate entity between tire and car"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)


class NewTire(models.Model):
    """New Tire entity"""
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    size = models.IntegerField()  # size types 14-22--> 0,1,2,3,4,5,6,7,8
    usage = models.IntegerField()  # summer-winter-snow-multipurpose--> 0,1,2,3
    p_num = models.IntegerField()
    price = models.FloatField()
    m_date = models.DateField()


class Reservation(models.Model):
    """Reservation Records"""

    Done = 1
    Waiting = 0
    Passed = 3
    RES_STATUS = (
        (Done, 'Done'),
        (Waiting, 'Waiting'),
        (Passed, 'Passed')
    )

    class Meta:
        unique_together = (('date', 'time', 'staff'),)

    date = models.DateField()
    time = models.TimeField()
    process = models.IntegerField()
    notify = models.BooleanField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff')
    status = models.IntegerField(choices=RES_STATUS, default=0)
