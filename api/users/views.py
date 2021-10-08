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


class ProfileList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, MyPermissionAdmin)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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
