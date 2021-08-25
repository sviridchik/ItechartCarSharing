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
    path('users/&', views.UserList.as_view(), name='users'),
    # url(r'^(?P<pk>[0-9]+|me)/defaults/campaign/$'
    # re_path('users/(?P<pk>\d)|(?P<me>me)', views.users_get_pk, name='users_me'),
    # path('users/(?P<pk>\d)+|me', views.UserDetailList.as_view, name='users_me'),
    re_path('users/(?P<pk>\d)|(?P<me>me)', views.UserDetailList.as_view(), name='users_me'),

]
