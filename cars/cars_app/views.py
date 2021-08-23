from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView, CreateAPIView, ListCreateAPIView
from django.contrib.auth.hashers import make_password
from .serializer import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.urls import reverse
from math import cos, asin, sqrt, pi
import datetime
from main.models import Profile
from price.models import *
from price.serializer import *
from trip.models import *
from trip.serializer import *
from .models import *

# Create your views here.

class CarList(CreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def is_admin(self, request):
        pk_user = request.user.id
        user_profile = Profile.objects.get(pk=pk_user)
        if not user_profile.is_admin:
            return False
        else:
            return True

    def post(self, request):

        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        # # raise Exception(request.data)
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        car = Cars.objects.all()
        serializer = CarSerializer(car, many=True)
        # raise Exception(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CarListDetail(APIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def is_admin(self, request):
        pk_user = request.user.id
        user_profile = Profile.objects.get(pk=pk_user)
        if not user_profile.is_admin:
            return False
        else:
            return True

    def get_object(self, pk):
        try:
            return Cars.objects.get(pk=pk)
        except Cars.DoesNotExist:
            return Response({"error": "there is no such price"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        car = self.get_object(pk)
        serializer = CarSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        car = self.get_object(pk)
        serializer = CarSerializer(car,
                                   data=request.data,
                                   partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        car = self.get_object(pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Хаверсин
def haversin(lat1, lon1, lat2, lon2):
    p = pi / 180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


@api_view(['GET'])
def get_free_cars(request):
    latitude = float(request.query_params.get('latitude'))
    longitude = float(request.query_params.get('longitude'))
    distance = float(request.query_params.get('distance'))
    class_car = request.query_params.get('class_car')
    ordering = request.query_params.get('ordering')
    disc_flag = False
    user = request.user

    res = []
    free_cars = Cars.objects.filter(status="free")

    already_seen = []
    cars_already_seen = ViewedCars.objects.all()
    for car in cars_already_seen:
        already_seen.append((car.user.id, car.car.id))

    for free_car in free_cars:
        car_lat = free_car.latitude
        car_lon = free_car.longitude
        s = haversin(latitude, longitude, car_lat, car_lon)
        if s <= distance and free_car.car_class.name == class_car:
            data_viewed = {}
            res.append({"car": dict(CarSerializer(free_car).data), "distance": s})
            data_viewed['car'] = free_car.id
            data_viewed['price_day'] = free_car.car_class.price.price_for_km
            data_viewed['price_night'] = free_car.car_class.price.price_for_km + free_car.car_class.price.night_add
            data_viewed['user'] = Profile.objects.get(user=user).id

            data_viewed['booking_price'] = free_car.car_class.price.booking_price
            if (data_viewed['car'], data_viewed['user']) not in already_seen:
                serializer = ViewedCarSerializer(data=data_viewed)
                if serializer.is_valid():
                    serializer.save()
    if ordering[0] == '-':
        disc_flag = True

    res.sort(key=lambda el: el["distance"], reverse=disc_flag)
    return Response(res, status=status.HTTP_200_OK)


# -------- Viewed cars -----------
class ViewedCarList(CreateAPIView):
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        car = ViewedCars.objects.all()
        serializer = ViewedCarSerializer(car, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewedCarListDetail(APIView):
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return ViewedCars.objects.get(pk=pk)
        except ViewedCars.DoesNotExist:
            return Response({"error": "there is no such price"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        car = self.get_object(pk)
        cars = ViewedCars.objects.all()
        for car in cars:
            car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#     -------------- book -----------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def to_book(request, pk):
    user = request.user
    # car status change
    Cars.objects.filter(pk=pk).update(status="free")

    try:
        car = Cars.objects.get(pk=pk)
        if car.status != "free":
            return Response({"error": "this car is not free"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    Cars.objects.filter(pk=pk).update(status="booked")

    # create trip price
    user_profile = Profile.objects.get(user=user)
    viewd_car = ViewedCars.objects.filter(user=user_profile, car=pk)
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
    cars = ViewedCars.objects.all()
    for c in cars:
        c.delete()

    # create trip
    pk_trip_price = TripPrice.objects.latest('id')
    data_trip = {
        'is_active': True,
        'user': Profile.objects.get(user=user).id,
        # 'user' : None,
        'car': pk,
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

    return Response({}, status=status.HTTP_200_OK)

