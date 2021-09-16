from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, CreateAPIView
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
class ProfileList(APIView):
    permission_classes = (IsAuthenticated, MyPermissionAdmin)

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# (тоже пусть пока побудет пока не исправлю)
# class ProfileList(APIView):
# class ProfileList(mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   generics.GenericAPIView):
#     permission_classes = (IsAuthenticated, MyPermissionAdmin)
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    # def get(self, request, format=None):
    #     profiles = Profile.objects.all()
    #     serializer = ProfileSerializer(profiles, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def get(self, request, *args, **kwargs):
    #     # return self.list(request, *args, **kwargs)
    #     serializer = ProfileSerializer(super().get_queryset(), many=True)
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # return Response(self.list(request, *args, **kwargs),status=status.HTTP_200_OK)


class SignUp(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = ProfileSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)


class LogoutApiView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


class ProfileDetailList(APIView):
    permission_classes = (IsAuthenticated, MyPermissionPkME)

    def get_serializer_class(self, *args, **kwargs):
        if args[0].is_admin:
            return ProfileSerializer
        else:
            return ProfileSerializerRedused

    # моя специфичная штука)
    def _get_object(self, class_data, request,kwargs,message):
        if 'me' in kwargs:
            pk = Profile.objects.get(user=request.user).pk
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        else:
            return Response({"error": "invaliud key attribute"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return class_data.objects.get(pk=pk)
        except class_data.DoesNotExist:
            return Response({"error": f"there is no such {message}"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        node = self._get_object(class_data=Profile, request=request, kwargs=kwargs,message="user")
        serializer = ProfileSerializer(node)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request,*args, **kwargs):

        node = self._get_object(class_data=Profile, request=request, kwargs=kwargs, message="user")
        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request,*args, **kwargs):
    # пока не исправила пусть побудет здесь
        # if admin can change all fields
        # allowed_val_user = ["username", "email"]
        # allowed_val_admin = ["username", "email", "date_of_birth", "dtp_times", "is_admin"]
        # allowed_val = None
        # tmp = Profile.objects.get(user= request.user)
        # if tmp.is_admin:
        #     allowed_val = allowed_val_admin
        # else:
        #     allowed_val = allowed_val_user
        # if not set(request.data.keys()).issubset(set(allowed_val)):
        #     return Response({"error": "invalid field"}, status=status.HTTP_400_BAD_REQUEST)

        node = self._get_object(class_data=Profile, request=request, kwargs=kwargs, message="user")
        serializer = self.get_serializer_class(node)(node,
                                       data=request.data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
