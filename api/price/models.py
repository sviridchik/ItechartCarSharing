from django.db import models
from main.models import BaseModel


class Price(BaseModel):
    price_for_km = models.FloatField(null=False, blank=False)
    night_add = models.FloatField(null=False, blank=False)
    price_dtp = models.FloatField(null=False, blank=False)
    parking_price = models.FloatField(null=False, blank=False)
    booking_price = models.FloatField(null=False, blank=False)
    description = models.TextField()
