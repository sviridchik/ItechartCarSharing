from cars_app.utils import pk_reg
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [

    path('/', views.TripList.as_view()),
    path('/trip_price', views.TripPriceList.as_view()),
    path('/trip_price/' + pk_reg, views.TripPriceListDetail.as_view()),
    path('/trip_log', views.LogList.as_view()),
]
