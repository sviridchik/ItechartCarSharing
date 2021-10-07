from rest_framework import serializers
from class_cars.serializers import ClassSerializer

from .models import *


class CarSerializer(serializers.ModelSerializer):
    car_class = ClassSerializer(read_only=True)

    class Meta:
        model = Cars
        fields = ('id', 'level_consumption', 'mark', 'reg_number', 'color', 'year', 'latitude', 'status', 'car_class',
                  'longitude')
        read_only_fields = ('id',)


class ViewedCarSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)


    class Meta:
        model = ViewedCars
        fields = ('id', 'car', 'price_day', 'price_night', 'user', 'booking_price')
        read_only_fields = ('id',)
