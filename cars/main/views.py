from django.shortcuts import redirect
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import MyPermissionAdmin, MyPermissionPkME
from .serializer import *


@api_view(['GET'])
def health(request):
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


class UserList(APIView):
    permission_classes = (IsAuthenticated, MyPermissionAdmin)

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = UserSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailList(APIView):
    permission_classes = (IsAuthenticated, MyPermissionPkME)

    def preparation(self, request, pk=None, me=None):
        pk_user = request.user.id
        self.is_admin_user = False
        pk_target = None
        if pk is not None:
            pk_target = pk
            if pk != pk_user:
                self.is_admin_user = True
        elif me is not None:
            pk_target = pk_user
        return pk_target

    def get_object(self, class_data, pk, message):

        try:
            return class_data.objects.get(pk=pk)
        except class_data.DoesNotExist:
            return Response({"error": f"there is no such {message}"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, me=None):
        profiles = Profile.objects.all()
        serializer = UserSerializer(profiles, many=True)
        # raise Exception(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, me=None):

        pk_target = self.preparation(request=request, pk=pk, me=me)
        node = self.get_object(class_data=Profile, pk=pk_target, message='user')

        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, me=None):
        pk_target = self.preparation(request=request, pk=pk, me=me)

        # if admin can change all fields
        allowed_val_admin = ["name", "email"]
        allowed_val_user = ["name", "email", "date_of_birth", "dtp_times", "is_admin"]
        allowed_val = None

        if self.is_admin_user:
            allowed_val = allowed_val_admin
        else:
            allowed_val = allowed_val_user
        if not set(request.data.keys()).issubset(set(allowed_val)):
            return Response({"error": "invalid field"}, status=status.HTTP_400_BAD_REQUEST)

        profile = self.get_object(class_data=Profile, pk=pk_target, message='user')
        serializer = UserSerializer(profile,
                                    data=request.data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
