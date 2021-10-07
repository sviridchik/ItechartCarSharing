from rest_framework import generics
from price.permissions import MyPermissionAdminNotUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import ClassCar
from .serializers import ClassSerializer


# Create your views here.

class ClassList(generics.ListCreateAPIView):
    queryset = ClassCar.objects.all()
    serializer_class = ClassSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdminNotUser)


class ClassListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassCar.objects.all()
    serializer_class = ClassSerializer
    permission_classes = (IsAuthenticated, MyPermissionAdminNotUser)
