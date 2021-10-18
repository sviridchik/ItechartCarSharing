import datetime
from django.shortcuts import render
from math import cos, asin, sqrt, pi
from price.permissions import MyPermissionAdminNotUser
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from trip.models import TripPrice, Trip, TripLog
from trip.serializer import TripSerializer, TripPriceSerializer, TripLogSerializer


# Create your views here.
class TripList(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = (IsAuthenticated)

    # -------------- trip price ---------------------


class TripPriceList(generics.CreateAPIView):
    queryset = TripPrice.objects.all()
    serializer_class = TripPriceSerializer
    permission_classes = (IsAuthenticated)


class TripPriceListDetail(generics.RetrieveDestroyAPIView):
    queryset = TripPrice.objects.all()
    serializer_class = TripPriceSerializer
    permission_classes = (IsAuthenticated)


# -------------- trip log ---------------------
class LogList(generics.RetrieveAPIView):
    queryset = TripLog.objects.all()
    serializer_class = TripLogSerializer
    permission_classes = [IsAuthenticated]
