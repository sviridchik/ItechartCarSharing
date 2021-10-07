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

from .permissions import MyPermissionAdmin, MyPermissionPkME
from .serializer import *

<< << << < HEAD


class ProfileList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, MyPermissionAdmin)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        birth_date = Profile.objects.get(user = request.user).date_of_birth
        if (date.today() - birth_date) // timedelta(days=365.2425) <18:
            return Response({"error": "under 18"},status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)

class SignUp(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)


class LogoutApiView(CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)


class ProfileDetailList(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, MyPermissionPkME)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_serializer_class(self, *args, **kwargs):
        if Profile.objects.get(user=self.request.user).is_admin:
            return ProfileSerializer
        else:
            return ProfileSerializerRedused



def get_object(self):
    if 'me' in self.kwargs:
        pk = Profile.objects.get(user=self.request.user).pk
    else:
        pk = self.kwargs['pk']
    try:
        return Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response({"error": "Not found!"}, status=status.HTTP_404_NOT_FOUND)
