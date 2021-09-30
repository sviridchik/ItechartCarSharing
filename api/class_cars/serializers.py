from rest_framework import serializers

from .models import *


class ClassSerializer(serializers.ModelSerializer):
    booking_time = serializers.IntegerField(min_value=0)

    class Meta:
        model = ClassCar
        fields = ('id', 'name', 'price', 'booking_time')
        read_only_fields = ('id',)
