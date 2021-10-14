from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [

    path('/', views.TripList.as_view()),
    path('/trip_price', views.TripPriceList.as_view()),
    path('/trip_price/<int:pk>', views.TripPriceListDetail.as_view()),
    path('/start/<int:pk>', views.trip_start),
    re_path('/(?P<pk>\d)/logs$', views.post_get_logs),
    re_path('/(?P<pk>\d)/logs/(?P<pk_log>\d)', views.TripLogListDetail.as_view()),
    path('/finish/', views.trip_finish),

]
