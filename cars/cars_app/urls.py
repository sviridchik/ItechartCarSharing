from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('', views.CarList.as_view()),
    path('/', views.CarList.as_view()),
    path('/<int:pk>', views.CarListDetail.as_view()),
    path('/free/', views.get_free_cars),
    path('/view/', views.ViewedCarList.as_view()),
    path('/view/<int:pk>', views.ViewedCarListDetail.as_view()),
    path('/<int:pk>/book', views.to_book),

]