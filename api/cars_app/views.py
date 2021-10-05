# Create your views here.
from math import cos, asin, sqrt, pi
import datetime
from price.models import *
from price.permissions import MyPermissionAdminNotUser
from price.serializer import *
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Profile
from rest_framework.decorators import api_view, permission_classes
from trip.serializer import TripPriceSerializer,TripSerializer,TripLogSerializer
from trip.models import TripPrice,Trip

from .serializer import *


class CarList(generics.ListCreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdminNotUser)


class CarListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdminNotUser)


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
    class_car = request.query_params.get('class')
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
class ViewedCarList(generics.ListAPIView):
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer
    permission_classes = (IsAuthenticated)


class ViewedCarListDetail(generics.DestroyAPIView):
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer
    permission_classes = (IsAuthenticated)


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
        return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
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
