# Create your views here.
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
from .utils import haversin


class CarList(generics.ListCreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdminNotUser)


class CarListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdminNotUser)


class FreeViewedCarsList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # serializer_class = ViewedCarSerializer
    serializer_class = FreeViewedCarSerializer

    def get_queryset(self):

        ordering = request.query_params.get('ordering')

        return super().get_queryset().filter(user=request.user).order_by(ordering)

    def list(self, request, *args, **kwargs):
        process_data = dict(request.query_params)

        for k, v in process_data.items():
            if k == 'class_car' or k == 'ordering':
                process_data[k] = v[0]
            else:
                process_data[k] = float(v[0])

        serializer_params = ParamsSerializer(process_data).data
        user = request.user
        profile = user.profile

        res = []
        free_cars = Cars.objects.filter(status=CarStatuses.FREE)

        # уже неважно
        already_seen = len(ViewedCars.objects.filter(user=profile))
        if already_seen > 0:
            already_seen.delete()

        for free_car in free_cars:
            car_lat = free_car.latitude
            car_lon = free_car.longitude
            s = haversin(serializer_params['latitude'], serializer_params['longitude'], car_lat, car_lon)
            if s <= serializer_params['distance'] and free_car.car_class.name == serializer_params['class_car']:
                data_viewed = {}
                res.append({"car": free_car, "distance": s})
                data_viewed['car'] = free_car.id
                data_viewed['price_day'] = free_car.car_class.price.price_for_km
                data_viewed['price_night'] = free_car.car_class.price.price_for_km + free_car.car_class.price.night_add
                data_viewed['user'] = profile.id
                data_viewed['booking_price'] = free_car.car_class.price.booking_price
                serializer = ViewedCarSerializer(data=data_viewed)
                if serializer.is_valid():
                    serializer.save()
        data_res = FreeViewedCarSerializer(res, many=True)
        return Response(data_res.data, status=status.HTTP_200_OK)


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
class Booking(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    # serializer_class = ViewedCarSerializer
    serializer_class = FreeViewedCarSerializer

    def post(self, request, *args, **kwargs):
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
            'user': Profile.objects.get(user=user).id,
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

        return Response({})


