from django.db import models
from main.models import BaseModel
from price.models import Price


# Create your models here.
class ClassCar(BaseModel):
    name = models.CharField(max_length=255)
    price = models.ForeignKey(Price, on_delete=models.SET_NULL, null=True)
    booking_time = models.IntegerField(blank=False)
