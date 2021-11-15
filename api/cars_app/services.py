import datetime
from math import cos, asin, sqrt, pi
from price.permissions import MyPermissionAdminNotUser
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from trip.models import TripPrice, Trip, TripLog
from trip.serializer import TripSerializer, TripPriceSerializer, TripLogSerializer
from users.models import Profile

from .models import CarStatuses
from .models import Cars, ViewedCars
from .serializer import ViewedCarSerializer, CarSerializer, ParamsSerializer, FreeViewedCarSerializer


def booking_logic(request, *args, **kwargs):
    user = request.user
    pk = kwargs['pk']
    try:
        car = ViewedCars.objects.get(pk=pk).car
        if car.status != CarStatuses.FREE:
            return Response({"error": "this car is not free"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    Cars.objects.filter(pk=car.id).update(status="booked")

    # create trip price
    user_profile = user.profile
    viewd_car = ViewedCars.objects.filter(user=user_profile, car=car.id)
    if len(viewd_car) == 0:
        return Response({"error": "no unavailable cars"}, status=status.HTTP_400_BAD_REQUEST)

    data_trip_price = {}
    data_trip_price['price_day'] = viewd_car[0].price_day / 1.0
    data_trip_price['price_night'] = viewd_car[0].price_night / 1.0
    data_trip_price['booking_price'] = viewd_car[0].booking_price / 1.0

    serializer = TripPriceSerializer(data=data_trip_price)
    if serializer.is_valid():
        serializer.save()

    # del viewed cars
    ViewedCars.objects.filter(user=user_profile).delete()

    # create trip
    pk_trip_price = TripPrice.objects.latest('id')
    data_trip = {
        'is_active': True,
        'user': user_profile.id,
        'car': car.id,
        'trip_price': pk_trip_price.id,
        'is_booked': True
    }
    serializer = TripSerializer(data=data_trip)
    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)
    # add log
    now = datetime.datetime.now()
    data_log = {'time_stamp': now.strftime("%H:%M"),
                'type': 'booked',
                'trip': Trip.objects.latest('id').id
                }
    serializer = TripLogSerializer(data=data_log)
    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)
