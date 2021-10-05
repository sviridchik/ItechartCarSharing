from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [


    path('trip/', views.TripList.as_view()),
    path('trip/trip_price', views.TripPriceList.as_view()),
    path('trip/trip_price/<int:pk>', views.TripPriceListDetail.as_view()),
    path('trip/trip_log', views.LogList.as_view()),

]