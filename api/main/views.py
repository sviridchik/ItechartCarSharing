from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import MyPermissionAdmin, MyPermissionPkME
from .serializer import *


@api_view(['GET'])
def health(request):
    return Response({}, status=status.HTTP_200_OK)


# class SignUp(CreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request,*args,**kwargs):
#         user = request.data
#         serializer = ProfileSerializer(data=user)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#
#         return Response(serializer.data,
#                         status=status.HTTP_201_CREATED)
#
#
# class LogoutApiView(GenericAPIView):
#     serializer_class = LogoutSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(status=status.HTTP_200_OK)


