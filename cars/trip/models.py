from django.db import models
from main.models import Profile
from cars_app.models import Cars
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
# Create your models here.
class TripPrice(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
    price_day = models.FloatField(blank=True)
    price_night = models.FloatField(blank=True)
    booking_price = models.FloatField(blank=True)


class Trip(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
    trip_price = models.ForeignKey(TripPrice, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Cars, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    final_price = models.IntegerField(blank=True,null=True)


class TripLog(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
    time_stamp = models.TimeField()
    type= models.CharField(max_length=255, choices=log_choose)
    trip= models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True)