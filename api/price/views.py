from django.shortcuts import render
from django.shortcuts import render
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
from .serializer import *

# Create your views here.
#  ------------------- price --------------------
class PriceList(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdmin)

class PriceListDetail(APIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsAuthenticated]

    # def is_admin(self, request):
    #     pk_user = request.user.id
    #     user_profile = Profile.objects.get(pk=pk_user)
    #     if not user_profile.is_admin:
    #         return False
    #     else:
    #         return True

    def get_object(self, pk):
        # Returns an object instance that should
        # be used for detail views.
        try:
            return Price.objects.get(pk=pk)
        except Price.DoesNotExist:
            return Response({"erroe":"there is no such price"}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not self.is_admin(request=request):
            return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
        price = self.get_object(pk)
        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
