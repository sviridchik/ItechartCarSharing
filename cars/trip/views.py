import datetime
from math import pi, cos, sqrt, asin

from django.shortcuts import render
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView, CreateAPIView, ListCreateAPIView
from .serializer import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from cars_app.models import ViewedCars,Cars
from main.models import *
from .models import *

# # Хаверсин
def haversin(lat1, lon1, lat2, lon2):
    p = pi / 180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

#

# Create your views here.

class TripList(CreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        trip = Trip.objects.all()
        serializer = TripSerializer(trip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------- trip price ---------------------
class TripPriceList(CreateAPIView):
    queryset = TripPrice.objects.all()
    serializer_class = TripPriceSerializer

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        trip = TripPrice.objects.all()
        serializer = TripPriceSerializer(trip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TripPriceListDetail(APIView):
    queryset = TripPrice.objects.all()
    serializer_class = TripPriceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return TripPrice.objects.get(pk=pk)
        except TripPrice.DoesNotExist:
            return Response({"error": "there is no such price"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        car = self.get_object(pk)
        serializer = TripPriceSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        car = self.get_object(pk)

        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trip_start(request, pk):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    flag_book = False
    id_book = None
    trip_book = None
    #     check wheather there are another active trips
    trips = Trip.objects.filter(user=user_profile)
    car_work = Cars.objects.get(pk=pk)
    for trip in trips:
        if trip.is_booked:
            flag_book = True
            id_book = trip.id
            trip_book = trip
        if trip.is_active and not trip.is_booked:
            return Response({"error": "finish previous trip please"}, status=status.HTTP_400_BAD_REQUEST)

    if not flag_book:
        # didn't booking then create trip price and trip
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
            'trip_price': pk_trip_price.id
        }
        serializer = TripSerializer(data=data_trip)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception(serializer.errors)

        # add log
        now = datetime.datetime.now()
        data_log = {'time_stamp': now.strftime("%H:%M"),
                    'type': 'start',
                    'trip': Trip.objects.latest('id').id
                    }
        serializer = TripLogSerializer(data=data_log)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception(serializer.errors)
    elif trip_book.car.id == pk:
        # add log
        now = datetime.datetime.now()
        data_log = {'time_stamp': now.strftime("%H:%M"),
                    'type': 'active',
                    'trip': id_book
                    }
        serializer = TripLogSerializer(data=data_log)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception(serializer.errors)
    else:
        return Response({"error": "you booked another car"}, status=status.HTTP_400_BAD_REQUEST)

    Cars.objects.filter(pk=pk).update(status="active")
    if trip_book:
        return Response(TripSerializer(trip_book).data, status=status.HTTP_200_OK)
    else:
        return Response(TripSerializer(Trip.objects.latest('id').id).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trip_finish(request):
    latitude = float(request.query_params.get('latitude'))
    longitude = float(request.query_params.get('longitude'))

    user = request.user
    user_profile = Profile.objects.get(user=user)

    if len(Trip.objects.filter(user=user_profile, is_active=True)) == 0:
        return Response({"error": "no active trips"}, status=status.HTTP_400_BAD_REQUEST)
    trip = Trip.objects.filter(user=user_profile, is_active=True)[0]
    car_work = Cars.objects.get(pk=trip.car.id)

    #     adding for booking
    if trip.is_booked:
        date = datetime.date(1, 1, 1)
        log_start = TripLog.objects.filter(trip=trip.id, type='start')[0].time_stamp
        log_booked = TripLog.objects.filter(trip=trip.id, type='booked')[0].time_stamp
        datetime1 = datetime.datetime.combine(date, log_start)

        datetime2 = datetime.datetime.combine(date, log_booked)

        time_book_total = datetime1 - datetime2
        booking_add = 0
        if time_book_total.total_seconds() / 60 > car_work.car_class.booking_time:
            booking_add = car_work.car_class.price.booking_price * time_book_total.total_seconds() / 60

    # day or night
    day_flag = False
    if datetime.datetime.today().strftime("%p") == "AM":
        day_flag = True
    #         calculate distanse of trip
    disctance_trip = haversin(car_work.latitude, car_work.longitude, latitude, longitude)

    # day or night
    price_distance = car_work.car_class.price.price_for_km * disctance_trip

    if datetime.datetime.today().strftime("%p") != "AM":
        price_distance += car_work.car_class.price.night_add

    #         final price and status

    Trip.objects.filter(user=user_profile, is_active=True).update(final_price=price_distance + booking_add)
    Trip.objects.filter(user=user_profile, is_active=True).update(is_active=False)

    # create log
    now = datetime.datetime.now()

    data_log = {'time_stamp': now.strftime("%H:%M"),
                'type': 'finished',
                'trip': trip.id
                }
    serializer = TripLogSerializer(data=data_log)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # car status
    Cars.objects.filter(pk=trip.car.id).update(status="free")
    return Response(TripSerializer(trip).data, status=status.HTTP_201_CREATED)


# +++++++++++++++++++++++++++++++++++++++++++++++ logs ++++++++++++++++++++++++++++++++++++=


def is_admin(request):
    pk_user = request.user.id
    user_profile = Profile.objects.get(pk=pk_user)
    if not user_profile.is_admin:
        return False
    else:
        return True


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def post_get_logs(request, pk):
    if request.method == 'POST':
        if not is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        tmp_data = dict(request.data)
        now = datetime.datetime.now()

        tmp_data['trip'] = pk
        tmp_data['time_stamp'] = now.strftime("%H:%M")
        if type(tmp_data['type']) == list:
            tmp_data['type'] = tmp_data['type'][0]

        serializer = TripLogSerializer(data=tmp_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        logs = TripLog.objects.filter(trip=pk)
        serializer = TripLogSerializer(logs, many=True)
        # raise Exception(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TripLogListDetail(APIView):
    queryset = TripLog.objects.all()
    serializer_class = TripLogSerializer
    permission_classes = [IsAuthenticated]

    # raise Exception("hi")
    def is_admin(self, request):
        pk_user = request.user.id
        user_profile = Profile.objects.get(pk=pk_user)
        if not user_profile.is_admin:
            return False
        else:
            return True

    def get_object(self, pk, pk_log):
        try:
            return TripLog.objects.filter(trip=pk, pk=pk_log)[0]
        except TripLog.DoesNotExist:
            return Response({"error": "there is no such log"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, pk_log):

        log = self.get_object(pk, pk_log)
        serializer = TripLogSerializer(log)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, pk_log):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        log = self.get_object(pk, pk_log)
        serializer = TripLogSerializer(log,
                                       data=request.data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


