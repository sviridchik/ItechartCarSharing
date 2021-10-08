from class_cars.models import ClassCar
from django.db import models
from main.models import BaseModel
from users.models import Profile

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


class CarStatuses:
    FREE = 'free'
    UNAVALIABLE = 'unavaliable'
    BOOKED = 'booked'
    ACTIVE = 'active'


# Create your models here.

class Cars(BaseModel):
    level_consumption = models.IntegerField()
    mark = models.CharField(max_length=255, choices=mark_choose)
    reg_number = models.CharField(max_length=255)
    color = models.CharField(max_length=255, choices=color_choose)
    year = models.IntegerField(blank=False)
    latitude = models.FloatField(blank=True)
    status = models.CharField(max_length=255, choices=(
        ('free', CarStatuses.FREE), ('active', CarStatuses.ACTIVE), ('booked', CarStatuses.BOOKED),
        ('unavaliable', CarStatuses.UNAVALIABLE)))
    car_class = models.ForeignKey(ClassCar, on_delete=models.SET_NULL, null=True)
    longitude = models.FloatField(blank=True)


class ViewedCars(BaseModel):
    car = models.ForeignKey(Cars, on_delete=models.SET_NULL, null=True)
    price_day = models.IntegerField(blank=False)
    price_night = models.IntegerField(blank=False)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    booking_price = models.IntegerField(blank=False)
