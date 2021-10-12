from class_cars.models import ClassCar
from django.db import models
from main.models import BaseModel
from users.models import Profile


class Marks:
    M = "Mercedes-Benz"
    T = "Toyota"
    H = "Honda"


mark_choose = (
    (Marks.M, "Mercedes-Benz"),
    (Marks.T, "Toyota"),
    (Marks.H, "Honda"),
)


class Colors:
    y = "yellow"
    w = "white"
    g = "green"


color_choose = (
    (Colors.y, "yellow"),
    (Colors.w, "white"),
    (Colors.g, "green"),
)


class Statuses:
    BOOKED = 'booked'
    FINISHED = 'finished'
    ACTIVE = 'active'


status_choose = (
    (Statuses.ACTIVE, "active"),
    (Statuses.FINISHED, "finished"),
    (Statuses.BOOKED, "booked"),
)


class LogStatuses:
    ACTIVE = "active"
    FINISHED = "finished"
    BOOKED = "booked"
    STOP = "stop"
    START = "start"


log_choose = (
    (LogStatuses.ACTIVE, "active"),
    (LogStatuses.FINISHED, "finished"),
    (LogStatuses.BOOKED, "booked"),
    (LogStatuses.STOP, "stop"),
    (LogStatuses.START, "start"),
)


class CarStatuses:
    FREE = 'free'
    UNAVALIABLE = 'unavaliable'
    BOOKED = 'booked'
    ACTIVE = 'active'


car_choose = (
    (CarStatuses.FREE, 'free'),
    (CarStatuses.ACTIVE, 'active'),
    (CarStatuses.BOOKED, 'booked'),
    (CarStatuses.UNAVALIABLE, 'unavaliable'))


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
    car = models.ForeignKey(Cars, on_delete=models.SET_NULL, null=True)
    price_day = models.IntegerField(blank=False)
    price_night = models.IntegerField(blank=False)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    booking_price = models.IntegerField(blank=False)
