from django.db import models
from main.models import BaseModel
from price.models import Price
# Create your models here.
class Class_car(BaseModel):
    # id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
    name = models.CharField(max_length=255)
    price = models.ForeignKey(Price,on_delete=models.SET_NULL,null = True)
    booking_time = models.IntegerField(blank=False)
