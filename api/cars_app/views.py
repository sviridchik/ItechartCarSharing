# Create your views here.
from math import cos, asin, sqrt, pi
from price.permissions import MyPermissionAdminNotUser
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from users.models import Profile

from .models import Cars, ViewedCars
from .serializer import ViewedCarSerializer, CarSerializer
from .utils import haversin


class CarList(generics.ListCreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdminNotUser)


class CarListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdminNotUser)


# Хаверсин
# def haversin(lat1, lon1, lat2, lon2):
#     p = pi / 180
#     a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
#     return 12742 * asin(sqrt(a))

class FreeCarsList(generics.ListAPIView):
    permission_classes = (AllowAny)
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer

    def get_object(self):

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
        cars_already_seen = ViewedCars.objects.filter(user=user)
        for car in cars_already_seen:
            already_seen.append((car.user.id, car.car.id))

        for free_car in free_cars:

            if free_car.car_class.name == class_car and haversin(latitude, longitude, free_car.latitude,
                                                                 free_car.longitude) <= distance:

                data_viewed = {}
                res.append(CarSerializer(free_car))
                # res.append({'car': dict(CarSerializer(free_car).data), 'distance': s})
                data_viewed['car'] = free_car.id
                data_viewed['price_day'] = free_car.car_class.price.price_for_km
                data_viewed['price_night'] = free_car.car_class.price.price_for_km + free_car.car_class.price.night_add
                # data_viewed['user'] = Profile.objects.get(user=user).id
                data_viewed['user'] = user.id
                data_viewed['booking_price'] = free_car.car_class.price.booking_price
                if (data_viewed['car'], data_viewed['user']) not in already_seen:
                    serializer = ViewedCarSerializer(data=data_viewed)
                    if serializer.is_valid():
                        serializer.save()
        if ordering[0] == '-':
            disc_flag = True

        res.sort(key=lambda el: el["distance"], reverse=disc_flag)
        return res

        # if 'me' in self.kwargs:
        #     pk = Profile.objects.get(user=self.request.user).pk
        # else:
        #     pk = self.kwargs['pk']
        # try:
        #     return Profile.objects.get(pk=pk)
        # except Profile.DoesNotExist:
        #     return Response({"error": "Not found!"}, status=status.HTTP_404_NOT_FOUND)

    # def get_free_cars(request):
    #     # latitude = float(request.query_params.get('latitude'))
    #     # longitude = float(request.query_params.get('longitude'))
    #     # distance = float(request.query_params.get('distance'))
    #     # class_car = request.query_params.get('class')
    #     # ordering = request.query_params.get('ordering')
    #     # disc_flag = False
    #     # user = request.user
    #
    #     res = []
    #     free_cars = Cars.objects.filter(status="free")
    #
    #     already_seen = []
    #     cars_already_seen = ViewedCars.objects.all()
    #     for car in cars_already_seen:
    #         already_seen.append((car.user.id, car.car.id))
    #
    #     for free_car in free_cars:
    #         car_lat = free_car.latitude
    #         car_lon = free_car.longitude
    #         s = haversin(latitude, longitude, car_lat, car_lon)
    #         if s <= distance and free_car.car_class.name == class_car:
    #             data_viewed = {}
    #             res.append({"car": dict(CarSerializer(free_car).data), "distance": s})
    #             data_viewed['car'] = free_car.id
    #             data_viewed['price_day'] = free_car.car_class.price.price_for_km
    #             data_viewed['price_night'] = free_car.car_class.price.price_for_km + free_car.car_class.price.night_add
    #             data_viewed['user'] = Profile.objects.get(user=user).id
    #
    #             data_viewed['booking_price'] = free_car.car_class.price.booking_price
    #             if (data_viewed['car'], data_viewed['user']) not in already_seen:
    #                 serializer = ViewedCarSerializer(data=data_viewed)
    #                 if serializer.is_valid():
    #                     serializer.save()
    #     if ordering[0] == '-':
    #         disc_flag = True
    #
    #     res.sort(key=lambda el: el["distance"], reverse=disc_flag)
    #
    #     return Response(res, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def get_free_cars(request):
#     latitude = float(request.query_params.get('latitude'))
#     longitude = float(request.query_params.get('longitude'))
#     distance = float(request.query_params.get('distance'))
#     class_car = request.query_params.get('class')
#     ordering = request.query_params.get('ordering')
#     disc_flag = False
#     user = request.user
#
#     res = []
#     free_cars = Cars.objects.filter(status="free")
#
#     already_seen = []
#     cars_already_seen = ViewedCars.objects.all()
#     for car in cars_already_seen:
#         already_seen.append((car.user.id, car.car.id))
#
#     for free_car in free_cars:
#         car_lat = free_car.latitude
#         car_lon = free_car.longitude
#         s = haversin(latitude, longitude, car_lat, car_lon)
#         if s <= distance and free_car.car_class.name == class_car:
#             data_viewed = {}
#             res.append({"car": dict(CarSerializer(free_car).data), "distance": s})
#             data_viewed['car'] = free_car.id
#             data_viewed['price_day'] = free_car.car_class.price.price_for_km
#             data_viewed['price_night'] = free_car.car_class.price.price_for_km + free_car.car_class.price.night_add
#             data_viewed['user'] = Profile.objects.get(user=user).id
#
#             data_viewed['booking_price'] = free_car.car_class.price.booking_price
#             if (data_viewed['car'], data_viewed['user']) not in already_seen:
#                 serializer = ViewedCarSerializer(data=data_viewed)
#                 if serializer.is_valid():
#                     serializer.save()
#     if ordering[0] == '-':
#         disc_flag = True
#
#     res.sort(key=lambda el: el["distance"], reverse=disc_flag)
#     return Response(res, status=status.HTTP_200_OK)


# -------- Viewed cars -----------
class ViewedCarList(generics.ListAPIView):
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer
    permission_classes = (IsAuthenticated)


class ViewedCarListDetail(generics.DestroyAPIView):
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer
    permission_classes = (IsAuthenticated)
