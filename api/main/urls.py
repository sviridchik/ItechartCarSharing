from django.urls import path, include, re_path
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from main import views

urlpatterns = [
    path('health/', views.health, name='health'),
    path('auth/', include('djoser.urls.jwt')),
    # path('users/signin', TokenObtainPairView.as_view(), name='signin'),
    # path('users/signup', views.SignUp.as_view(), name='signup'),
    # path('users/logout', views.LogoutApiView.as_view(), name='logout'),
    # path('users/&', views.ProfileList.as_view(), name='users'),
    # # re_path('users/(?P<pk>\d)|(?P<me>me)', views.ProfileDetailList.as_view(), name='users_me'),
    # re_path('users/(?P<pk>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})|(?P<me>me)', views.ProfileDetailList.as_view(), name='users_me'),

]