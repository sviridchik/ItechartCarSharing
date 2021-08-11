from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView, CreateAPIView
from django.contrib.auth.hashers import make_password
from .serializer import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.urls import reverse
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
        return Response(data={"name ": n,"email":user_saved.email,'date_of_birth':user_saved.date_of_birth},status=status.HTTP_201_CREATED)



class LogoutApiView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)


    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_get(request):
# auth_part
    user = request.user
    user_profile = Profile.objects.get(pk=user.id)

    if not user_profile.is_admin:
        return Response({"error":"no rignts"}, status=status.HTTP_401_UNAUTHORIZED)
#end
    res  = {}
    try:
        dataProfile = Profile.objects.all()
        for e in dataProfile:
             res[e.id]={"name ": e.user.username, "email": e.email, 'date_of_birth': e.date_of_birth,"dtp_times":e.dtp_times,"is_admin":e.is_admin}
        # raise Exception(res)
    except Exception as e:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    return Response(res, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def users_get_pk(request,pk):
    # auth_part
    user = request.user
    # raise Exception(user.id)
    user_profile = Profile.objects.get(pk=pk)
    # user_profile = Profile.objects.get(pk=1)

    if not user_profile.is_admin:
        return Response({"error":"no rignts"}, status=status.HTTP_400_BAD_REQUEST)

    res  = {}
    try:
        dataProfile = Profile.objects.all()
        for e in dataProfile:
             res[e.id]={"name ": e.user.username, "email": e.email, 'date_of_birth': e.date_of_birth,"dtp_times":e.dtp_times,"is_admin":e.is_admin}
        # raise Exception(res)
    except Exception as e:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    return Response(res, status=status.HTTP_200_OK)