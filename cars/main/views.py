from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
        return Response(data={"name ": n, "email": user_saved.email, 'date_of_birth': user_saved.date_of_birth},
                        status=status.HTTP_201_CREATED)


class LogoutApiView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_get(request):
    # auth_part
    user = request.user
    user_profile = Profile.objects.get(pk=user.id)

    if not user_profile.is_admin:
        return Response({"error": "no rignts"}, status=status.HTTP_401_UNAUTHORIZED)
    # end
    res = {}
    try:
        dataProfile = Profile.objects.all()
        for e in dataProfile:
            res[e.id] = {"name ": e.user.username, "email": e.email, 'date_of_birth': e.date_of_birth,
                         "dtp_times": e.dtp_times, "is_admin": e.is_admin}
        # raise Exception(res)
    except Exception as e:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    return Response(res, status=status.HTTP_200_OK)


@api_view(['PATCH', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def users_get_pk(request, pk=None, me=None):
    is_admin_user = False
    # raise Exception(pk,me)
    pk_user = request.user.id
    user_profile = Profile.objects.get(pk=pk_user)
    pk_target = None
    if pk is not None:
        pk = int(pk)
        # not me ,then admin
        if pk != pk_user:
            if not user_profile.is_admin:
                return Response({"error": "no rights"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                pk_target = pk
                is_admin_user = True
        else:
            pk_target = pk
    elif me is not None:
        pk_target = pk_user
    if request.method == 'GET':
        res = {}
        try:
            e = Profile.objects.get(pk=pk_target)
            res[e.id] = {"name ": e.user.username, "email": e.email, 'date_of_birth': e.date_of_birth,
                         "dtp_times": e.dtp_times, "is_admin": e.is_admin}
            # raise Exception(res)
        except Exception as ex:
            return Response({"error": ex}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        # if admin can change all fields
        allowed_val_admin = ["name", "email"]
        allowed_val_user = ["name", "email", "date_of_birth", "dtp_times", "is_admin"]
        allowed_val = None

        if is_admin_user:
            allowed_val = allowed_val_admin
        else:
            allowed_val = allowed_val_user

        for field in request.data.keys():
            val = request.data[field]
            if field in allowed_val:
                if field == "name":
                    Profile.objects.filter(pk=pk_target).update(username=val)
                elif field == "email":
                    Profile.objects.filter(pk=pk_target).update(email=val)
                elif field == "date_of_birth":
                    Profile.objects.filter(pk=pk_target).update(date_of_birth=val)
                elif field == "dtp_times":
                    Profile.objects.filter(pk=pk_target).update(dtp_times=val)
                elif field == "is_admin":
                    Profile.objects.filter(pk=pk_target).update(is_admin=val)

            else:
                return Response({"error": "invalid field"}, status=status.HTTP_400_BAD_REQUEST)
        res = {}
        try:
            node = Profile.objects.get(pk=pk_target)
            res[node.id] = {"name ": node.user.username, "email": node.email, 'date_of_birth': node.date_of_birth,
                            "dtp_times": node.dtp_times, "is_admin": node.is_admin}
        except Exception as ex:
            return Response({"error": ex}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':

        res = {}
        node = Profile.objects.get(pk=pk_target)
        res[node.id] = {"name ": node.user.username, "email": node.email, 'date_of_birth': node.date_of_birth,
                        "dtp_times": node.dtp_times, "is_admin": node.is_admin}
        Profile.objects.filter(pk=pk_target).delete()

        return Response(res, status=status.HTTP_200_OK)