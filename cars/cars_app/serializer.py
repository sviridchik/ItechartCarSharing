from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *



class CarSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cars
        fields = ('id', 'level_consumption', 'mark', 'reg_number', 'color', 'year', 'latitude', 'status', 'car_class',
                  'longitude')
        read_only_fields = ('id',)


class ViewedCarSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ViewedCars
        fields = ('id', 'car', 'price_day', 'price_night', 'user', 'booking_price')
        read_only_fields = ('id',)

