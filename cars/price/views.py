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

from .models import *

# Create your views here.

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

