from django.db import models
import sys

# from cars.class_car.models import Class_car

sys.path.append("..")
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# from price.models import *
# from class_car.models import *
# from cars_app.models import *

mark_choose = (
    ("Mercedes-Benz", "Mercedes-Benz"),
    ("Toyota", "Toyota"),
    ("Honda", "Honda"),
)

color_choose = (
    ("y", "yellow"),
    ("w", "white"),
    ("g", "green"),
)

status_choose = (
    ("active", "active"),
    ("finished", "finished"),
    ("booked", "booked"),
)

log_choose = (
    ("active", "active"),
    ("finished", "finished"),
    ("booked", "booked"),
    ("stop", "stop"),
    ("start", "start"),
)
car_choose = (
    ("active", "active"),
    ("free", "free"),
    ("booked", "booked"),
)

# class_car Price(models.Model):
#     id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
#     price_for_km = models.FloatField(blank=True)
#     night_add = models.FloatField(blank=True)
#     price_dtp = models.FloatField(blank=True)
#     parking_price = models.FloatField(blank=True)
#     booking_price = models.FloatField(blank=True)
#     description = models.TextField()
#
#
# class Class_car(models.Model):
#     id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
#     name = models.CharField(max_length=255)
#     price = models.ForeignKey(Price, on_delete=models.SET_NULL, null=True)
#     booking_time = models.IntegerField(blank=False)
#
# #
# class Cars(models.Model):
#     id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
#     level_consumption = models.IntegerField()
#     mark = models.CharField(max_length=255, choices=mark_choose)
#     reg_number = models.CharField(max_length=255)
#     color = models.CharField(max_length=255, choices=color_choose)
#     year = models.IntegerField(blank=False)
#     latitude = models.FloatField(blank=True)
#     status = models.CharField(max_length=255, choices=car_choose)
#     car_class = models.ForeignKey(Class_car, on_delete=models.SET_NULL, null=True)
#     longitude = models.FloatField(blank=True)

#
# # # Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
    date_of_birth = models.DateField(verbose_name='date_of_birth')
    email = models.CharField(max_length=255, verbose_name="email")
    is_admin = models.BooleanField(verbose_name='is_admin', default=False)
    dtp_times = models.IntegerField(verbose_name='dtp_times', default=0)

# #
# class ViewedCars(models.Model):
#     id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
#     car = models.ForeignKey(Cars, on_delete=models.SET_NULL, null=True)
#     price_day = models.IntegerField(blank=False)
#     price_night = models.IntegerField(blank=False)
#     user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
#     booking_price = models.IntegerField(blank=False)
#

# class TripPrice(models.Model):
#     id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
#     price_day = models.FloatField(blank=True)
#     price_night = models.FloatField(blank=True)
#     booking_price = models.FloatField(blank=True)
#
#
# class Trip(models.Model):
#     id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
#     trip_price = models.ForeignKey(TripPrice, on_delete=models.SET_NULL, null=True)
#     user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
#     car = models.ForeignKey(Cars, on_delete=models.SET_NULL, null=True)
#     is_active = models.BooleanField(default=False)
#     is_booked = models.BooleanField(default=False)
#     final_price = models.IntegerField(blank=True,null=True)
#
#
# class TripLog(models.Model):
#     id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
#     time_stamp = models.TimeField()
#     type= models.CharField(max_length=255, choices=log_choose)
#     trip= models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True)
