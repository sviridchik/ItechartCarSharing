# Create your views here.
from math import cos, asin, sqrt, pi
from price.permissions import MyPermissionAdminNotUser
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from users.models import Profile

from .models import CarStatuses
from .models import Cars, ViewedCars
from .serializer import ViewedCarSerializer, CarSerializer, ParamsSerializer,FreeViewedCarSerializer
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
    permission_classes = (AllowAny)
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer


@api_view(['GET'])
def get_free_cars(request):
    process_data = dict(request.query_params)

    for k, v in process_data.items():
        if k == 'class_car' or k == 'ordering':
            process_data[k] = v[0]
        else:
            process_data[k] = float(v[0])

    serializer_params = ParamsSerializer(process_data).data
    disc_flag = False
    user = request.user
    profile = user.profile

    res = []
    free_cars = Cars.objects.filter(status=CarStatuses.FREE)

    # уже неважно
    already_seen = len(ViewedCars.objects.all())
    if already_seen > 0:
        already_seen.delete()

    for free_car in free_cars:
        car_lat = free_car.latitude
        car_lon = free_car.longitude
        s = haversin(serializer_params['latitude'], serializer_params['longitude'], car_lat, car_lon)
        if s <= serializer_params['distance'] and free_car.car_class.name == serializer_params['class_car']:
            data_viewed = {}
            # res.append({"car": dict(CarSerializer(free_car).data), "distance": s})
            res.append({"car": free_car, "distance": s})
            data_viewed['car'] = free_car.id
            data_viewed['price_day'] = free_car.car_class.price.price_for_km
            data_viewed['price_night'] = free_car.car_class.price.price_for_km + free_car.car_class.price.night_add
            data_viewed['user'] = profile.id
            data_viewed['booking_price'] = free_car.car_class.price.booking_price
            serializer = ViewedCarSerializer(data=data_viewed)
            if serializer.is_valid():
                serializer.save()
    if serializer_params['ordering'][0] == '-':
        disc_flag = True
    data_res = FreeViewedCarSerializer(res,many = True)
    res.sort(key=lambda el: el["distance"], reverse=disc_flag)
    return Response(data_res.data, status=status.HTTP_200_OK)
    # return res


# -------- Viewed cars -----------
class ViewedCarList(generics.ListAPIView):
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer
    permission_classes = (IsAuthenticated)


class ViewedCarListDetail(generics.DestroyAPIView):
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer
    permission_classes = (IsAuthenticated)
