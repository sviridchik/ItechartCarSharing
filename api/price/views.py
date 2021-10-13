from django.shortcuts import render
from django.shortcuts import render
from price.permissions import MyPermissionAdminNotUser
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Profile
from users.permissions import MyPermissionAdmin, MyPermissionPkME

from .models import Price
from .serializer import PriceSerializer


# Create your views here.
class PriceList(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdmin)


class PriceListDetail(RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdminNotUser)
