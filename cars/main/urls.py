from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('health/', views.health, name='health'),
    path('auth/', include('djoser.urls.jwt')),
    path('users/signin', TokenObtainPairView.as_view(), name='signin'),
    path('users/signup', views.SignUp.as_view(), name='signup'),
    path('users/logout', views.LogoutApiView.as_view(), name='logout'),
    path('users/', views.UserList.as_view(), name='users'),
    re_path('users/(?P<pk>\d)|(?P<me>me)', views.users_get_pk, name='users_me'),
]
