
from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

from .views import PriceList,PriceListDetail

urlpatterns = [


# path('price', views.PriceList.as_view()),
# path('price/', views.PriceList.as_view()),
# path('price/<int:pk>', views.PriceListDetail.as_view()),

path('', PriceList.as_view()),
path('/', PriceList.as_view()),
path('/<int:pk>', PriceListDetail.as_view()),
]