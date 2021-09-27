from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView, ListCreateAPIView
from django.contrib.auth.hashers import make_password
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import datetime
from users.models import Profile
from price.models import *

from .models import *
# Create your views here.

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
