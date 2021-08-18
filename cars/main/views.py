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

from .models import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def change(request):
    user = request.user
    return Response({}, status=status.HTTP_200_OK)


def change_red(request):
    return redirect("/health")


class SignUp(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        n = str(user_saved.user)
        return Response(data={"name ": n, "email": user_saved.email, 'date_of_birth': user_saved.date_of_birth},
                        status=status.HTTP_201_CREATED)


class LogoutApiView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_get(request):
    # auth_part
    user = request.user
    user_profile = Profile.objects.get(pk=user.id)

    if not user_profile.is_admin:
        return Response({"error": "no rignts"}, status=status.HTTP_401_UNAUTHORIZED)
    # end
    res = {}
    try:
        dataProfile = Profile.objects.all()
        for e in dataProfile:
            res[e.id] = {"name ": e.user.username, "email": e.email, 'date_of_birth': e.date_of_birth,
                         "dtp_times": e.dtp_times, "is_admin": e.is_admin}
        # raise Exception(res)
    except Exception as e:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    return Response(res, status=status.HTTP_200_OK)


@api_view(['PATCH', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def users_get_pk(request, pk=None, me=None):
    is_admin_user = False
    # raise Exception(pk,me)
    pk_user = request.user.id
    user_profile = Profile.objects.get(pk=pk_user)
    pk_target = None
    if pk is not None:
        pk = int(pk)
        # not me ,then admin
        if pk != pk_user:
            if not user_profile.is_admin:
                return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                pk_target = pk
                is_admin_user = True
        else:
            pk_target = pk
    elif me is not None:
        pk_target = pk_user
    if request.method == 'GET':
        res = {}
        try:
            e = Profile.objects.get(pk=pk_target)
            res[e.id] = {"name ": e.user.username, "email": e.email, 'date_of_birth': e.date_of_birth,
                         "dtp_times": e.dtp_times, "is_admin": e.is_admin}
            # raise Exception(res)
        except Exception as ex:
            return Response({"error": ex}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        # if admin can change all fields
        allowed_val_admin = ["name", "email"]
        allowed_val_user = ["name", "email", "date_of_birth", "dtp_times", "is_admin"]
        allowed_val = None

        if is_admin_user:
            allowed_val = allowed_val_admin
        else:
            allowed_val = allowed_val_user

        for field in request.data.keys():
            val = request.data[field]
            if field in allowed_val:
                if field == "name":
                    Profile.objects.filter(pk=pk_target).update(username=val)
                elif field == "email":
                    Profile.objects.filter(pk=pk_target).update(email=val)
                elif field == "date_of_birth":
                    Profile.objects.filter(pk=pk_target).update(date_of_birth=val)
                elif field == "dtp_times":
                    Profile.objects.filter(pk=pk_target).update(dtp_times=val)
                elif field == "is_admin":
                    Profile.objects.filter(pk=pk_target).update(is_admin=val)

            else:
                return Response({"error": "invalid field"}, status=status.HTTP_400_BAD_REQUEST)
        res = {}
        try:
            node = Profile.objects.get(pk=pk_target)
            res[node.id] = {"name ": node.user.username, "email": node.email, 'date_of_birth': node.date_of_birth,
                            "dtp_times": node.dtp_times, "is_admin": node.is_admin}
        except Exception as ex:
            return Response({"error": ex}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':

        res = {}
        node = Profile.objects.get(pk=pk_target)
        res[node.id] = {"name ": node.user.username, "email": node.email, 'date_of_birth': node.date_of_birth,
                        "dtp_times": node.dtp_times, "is_admin": node.is_admin}
        Profile.objects.filter(pk=pk_target).delete()

        return Response(res, status=status.HTTP_200_OK)


# ------------------- price --------------------
class PriceList(CreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

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

        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        price = Price.objects.all()
        serializer = PriceSerializer(price, many=True)
        # raise Exception(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PriceListDetail(APIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
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
            return Price.objects.get(pk=pk)
        except Price.DoesNotExist:
            return Response({"erroe": "there is no such price"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        price = self.get_object(pk)
        serializer = PriceSerializer(price)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        price = self.get_object(pk)
        serializer = PriceSerializer(price,
                                     data=request.data,
                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        price = self.get_object(pk)
        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ------------------------------------------ class  ------------------------------------------------------------------


class ClassList(CreateAPIView):
    queryset = Class_car.objects.all()
    serializer_class = ClassSerializer

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

        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        class_car = Class_car.objects.all()
        serializer = ClassSerializer(class_car, many=True)
        # raise Exception(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassListDetail(APIView):
    queryset = Price.objects.all()
    serializer_class = ClassSerializer
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
            return Class_car.objects.get(pk=pk)
        except Class_car.DoesNotExist:
            return Response({"erroe": "there is no such price"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        class_car = self.get_object(pk)
        serializer = ClassSerializer(class_car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        class_car = self.get_object(pk)
        serializer = ClassSerializer(class_car,
                                     data=request.data,
                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        class_car = self.get_object(pk)
        class_car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ++++++++++++++++++++++++++++ cars ++++++++++++++++++++++++++++

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
    class_car = request.query_params.get('class')
    ordering = request.query_params.get('ordering')
    disc_flag = False
    user = request.user

    # user = None

    res = []
    free_cars = Cars.objects.filter(status="free")
    # raise Exception(free_cars)


    already_seen = []
    cars_already_seen = ViewedCars.objects.all()
    for car in cars_already_seen:
        # if user is :
        # already_seen.append((None,car.car.id))
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
            # data_viewed['user'] = None

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
        # raise Exception(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewedCarListDetail(APIView):
    queryset = ViewedCars.objects.all()
    serializer_class = ViewedCarSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        # Returns an object instance that should
        # be used for detail views.
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
def to_book(request, pk):
    user = request.user
    # user = None
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
    # viewd_car = ViewedCars.objects.filter(car=pk)
    if len(viewd_car) == 0:
        return Response({"error": "no unavailable cars"}, status=status.HTTP_400_BAD_REQUEST)

    # raise Exception(viewd_car)
    data_trip_price = {}
    data_trip_price['price_day'] = viewd_car[0].price_day / 1.0
    data_trip_price['price_night'] = viewd_car[0].price_night / 1.0
    data_trip_price['booking_price'] = viewd_car[0].booking_price / 1.0

    # raise Exception(data_trip_price['booking_price'])

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


# ++++++++++++++ trip ++++++++++++++++++++++
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
        # Returns an object instance that should
        # be used for detail views.
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


# -------------- trip log ---------------------
# class LogList(CreateAPIView):
#     queryset = TripLog.objects.all()
#     serializer_class = TripLogSerializer
#
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         trip = TripLog.objects.all()
#         serializer = TripLogSerializer(trip, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)




#     |||||||||||| trip ||||||||||||||||||||||
@api_view(['POST'])
def trip_start(request,pk):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    flag_book = False
    id_book = None
    trip_book = None
#     check wheather there are another active trips
    trips =  Trip.objects.filter(user=user_profile)
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
        # viewd_car = ViewedCars.objects.filter(car=pk)
        if len(viewd_car) == 0:
            return Response({"error": "no unavailable cars"}, status=status.HTTP_400_BAD_REQUEST)

        # raise Exception(viewd_car)
        data_trip_price = {}
        data_trip_price['price_day'] = viewd_car[0].price_day / 1.0
        data_trip_price['price_night'] = viewd_car[0].price_night / 1.0
        data_trip_price['booking_price'] = viewd_car[0].booking_price / 1.0

        # raise Exception(data_trip_price['booking_price'])

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
                    'type': 'active',
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

# +++++++++++++++++++++++++++++++++++++++++++++++ logs ++++++++++++++++++++++++++++++++++++=
# class TripLogList(CreateAPIView):
#     queryset = TripLog.objects.all()
#     serializer_class = TripLogSerializer
#     permission_classes = [IsAuthenticated]

def is_admin(self, request):
    pk_user = request.user.id
    user_profile = Profile.objects.get(pk=pk_user)
    if not user_profile.is_admin:
        return False
    else:
        return True

@api_view(['POST'])
def post_logs(self, request,pk,**kwargs):

    if not self.is_admin(request=request):
        return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
    # # raise Exception(request.data)
    request.data['trip'] = pk
    serializer = TripLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_logs(self, request, pk):
    logs = TripLog.objects.filter(trip = pk)
    serializer = TripLogSerializer(logs, many=True)
    # raise Exception(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


class TripLogListDetail(APIView):
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

    def get_object(self, pk, pk_log):
        try:
            return Cars.objects.get(pk=pk)
        except Cars.DoesNotExist:
            return Response({"error": "there is no such price"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk,pk_log):
        car = self.get_object(pk)
        serializer = CarSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, pk_log):
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

    def delete(self, request, pk, pk_log):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        car = self.get_object(pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
