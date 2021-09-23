from django.db import models
from main.models import BaseModel
# Create your models here.
class Price(BaseModel):
    # id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
    price_for_km = models.FloatField(blank=True)
    night_add = models.FloatField(blank=True)
    price_dtp = models.FloatField(blank=True)
    parking_price = models.FloatField(blank=True)
    booking_price = models.FloatField(blank=True)
    description = models.TextField()
