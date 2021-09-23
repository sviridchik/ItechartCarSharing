from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *


class PriceSerializer(serializers.ModelSerializer):
    price_for_km = serializers.FloatField(min_value=0)
    night_add = serializers.FloatField(min_value=0)
    price_dtp = serializers.FloatField(min_value=0)
    parking_price = serializers.FloatField(min_value=0)
    booking_price = serializers.FloatField(min_value=0)

    class Meta:
        model = Price
        fields = ('id', 'price_for_km', 'night_add', 'price_dtp', 'parking_price', 'booking_price', 'description')
