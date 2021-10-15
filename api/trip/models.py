from cars_app.models import Cars
from django.db import models
from main.models import BaseModel
from users.models import Profile


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


# Create your models here.
class TripPrice(BaseModel):
    price_day = models.FloatField(blank=True)
    price_night = models.FloatField(blank=True)
    booking_price = models.FloatField(blank=True)


class Trip(BaseModel):
    trip_price = models.ForeignKey(TripPrice, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Cars, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    final_price = models.IntegerField(blank=True, null=True)


class TripLog(BaseModel):
    time_stamp = models.TimeField()
    type = models.CharField(max_length=255, choices=log_choose)
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True)
