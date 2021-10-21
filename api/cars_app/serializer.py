from class_cars.serializers import ClassSerializer
from rest_framework import serializers

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
    price_day = serializers.FloatField(source = 'car.car_class.price.price_for_km')
    price_night = serializers.FloatField()
    class Meta:
        model = ViewedCars
        fields = ('id', 'car', 'price_day', 'price_night', 'user', 'booking_price')
        read_only_fields = ('id',)


class ParamsSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    distance = serializers.FloatField()
    class_car = serializers.CharField()
    ordering = serializers.CharField()


class FreeViewedCarSerializer(serializers.Serializer):
    car = CarSerializer(read_only=True,source = 'car')
    distance = serializers.FloatField(source = 'distance')

    # price_day=serializers.FloatField()
    #
    # data_viewed['price_day'] = free_car.car_class.price.price_for_km
    # data_viewed['price_night'] = free_car.car_class.price.price_for_km + free_car.car_class.price.night_add
    # data_viewed['user'] = profile.id
    # data_viewed['booking_price'] = free_car.car_class.price.booking_price

    class Meta:
        model = Cars
        fields = ('id', 'car', 'price_day', 'price_night', 'user', 'booking_price','distance')
        read_only_fields = ('id',)