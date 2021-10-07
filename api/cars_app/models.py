from django.db import models
from users.models import Profile
from class_cars.models import ClassCar
from main.models import BaseModel

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

class Cars(BaseModel):
    level_consumption = models.IntegerField()
    mark = models.CharField(max_length=255, choices=mark_choose)
    reg_number = models.CharField(max_length=255)
    color = models.CharField(max_length=255, choices=color_choose)
    year = models.IntegerField(blank=False)
    latitude = models.FloatField(blank=True)
    status = models.CharField(max_length=255, choices=car_choose)
    car_class = models.ForeignKey(ClassCar, on_delete=models.SET_NULL, null=True)
    longitude = models.FloatField(blank=True)


class ViewedCars(BaseModel):
    # id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
    car = models.ForeignKey(Cars, on_delete=models.SET_NULL, null=True)
    price_day = models.IntegerField(blank=False)
    price_night = models.IntegerField(blank=False)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    booking_price = models.IntegerField(blank=False)
