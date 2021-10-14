from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'email', 'dtp_times', 'username', 'password']

    def save(self, **kwargs):
        ps = make_password(self.data['password'])
        user = User.objects.create_user(self.data['username'], self.data['email'], self.data['password'])
        profile = Profile.objects.create(user=user, date_of_birth=self.data['date_of_birth'],
                                         email=self.data['email'],
                                         dtp_times=self.data['dtp_times'], )
        return profile


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

#
# class PriceSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     price_for_km = serializers.FloatField(min_value=0)
#     night_add = serializers.FloatField(min_value=0)
#     price_dtp = serializers.FloatField(min_value=0)
#     parking_price = serializers.FloatField(min_value=0)
#     booking_price = serializers.FloatField(min_value=0)
#
#     class Meta:
#         model = Price
#         fields = ('id', 'price_for_km', 'night_add', 'price_dtp', 'parking_price', 'booking_price', 'description')
#
#
# class ClassSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = Class_car
#         fields = ('id', 'name', 'price', 'booking_time')
#         read_only_fields = ('id',)

#
# class CarSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = Cars
#         fields = ('id', 'level_consumption', 'mark', 'reg_number', 'color', 'year', 'latitude', 'status', 'car_class',
#                   'longitude')
#         read_only_fields = ('id',)
#
#
# class ViewedCarSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = ViewedCars
#         fields = ('id', 'car', 'price_day', 'price_night', 'user', 'booking_price')
#         read_only_fields = ('id',)


# class TripSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = Trip
#         fields = ('id', 'car', 'trip_price', 'is_active', 'user', 'final_price','is_booked')
#         read_only_fields = ('id',)
#
#
# class TripPriceSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     price_day = serializers.FloatField()
#
#     class Meta:
#         model = TripPrice
#         fields = ('id', 'price_day', 'price_night', 'booking_price')
#         read_only_fields = ('id',)
#
#
# class TripLogSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = TripLog
#         fields = ('id', 'time_stamp', 'type', 'trip')
#         read_only_fields = ('id',)
