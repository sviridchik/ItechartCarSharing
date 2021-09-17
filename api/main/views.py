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
