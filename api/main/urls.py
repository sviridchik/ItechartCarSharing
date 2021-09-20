from django.urls import path, include, re_path
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from main import views

urlpatterns = [
    path('health/', views.health, name='health'),
    path('auth/', include('djoser.urls.jwt')),
]
