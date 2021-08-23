from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *



class TripSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = ('id', 'car', 'trip_price', 'is_active', 'user', 'final_price','is_booked')
        read_only_fields = ('id',)


class TripPriceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    price_day = serializers.FloatField()

    class Meta:
        model = TripPrice
        fields = ('id', 'price_day', 'price_night', 'booking_price')
        read_only_fields = ('id',)


class TripLogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = TripLog
        fields = ('id', 'time_stamp', 'type', 'trip')
        read_only_fields = ('id',)
