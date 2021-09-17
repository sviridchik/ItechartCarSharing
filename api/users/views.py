from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from .models import Profile
from .permissions import MyPermissionAdmin, MyPermissionPkME
from .serializer import *
from rest_framework import mixins
from rest_framework import generics


# Create your views here.

class ProfileList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, MyPermissionAdmin)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)


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

    # больше не моя специфичная штука)
    def get_object(self):
        if 'me' in self.kwargs:
            pk = Profile.objects.get(user=self.request.user).pk
        elif 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            return Response({"error": "invaliud key attribute"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({"error": f"there is no such user"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):

        node = self.get_object()
        serializer = self.get_serializer_class(node)(node,
                                                     data=request.data,
                                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
