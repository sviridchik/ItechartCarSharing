from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('health', views.change),
    path('health/', views.change_red),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/signin',TokenObtainPairView.as_view()),
    path('users/signup', views.SignUp.as_view()),
    path('users/logout',views.LogoutApiView.as_view()),
    path('users/',views.users_get),
    re_path('users/(?P<pk>\d)|(?P<me>me)$', views.users_get_pk),
    re_path('users/(?P<pk>\d)|(?P<me>me)/trip/current$', views.users_get_trip_current),
    re_path('users/(?P<pk>\d)|(?P<me>me)/trips$', views.users_get_trips),

    # path(r'^price', include('price.urls')),

    # path('price', views.PriceList.as_view()),
    # path('price/', views.PriceList.as_view()),
    # path('price/<int:pk>', views.PriceListDetail.as_view()),
    #
    # path('class_car', views.ClassList.as_view()),
    # path('class_car/', views.ClassList.as_view()),
    # path('class_car/<int:pk>', views.ClassListDetail.as_view()),


    # path('cars', views.CarList.as_view()),
    # path('cars/', views.CarList.as_view()),
    # path('cars/<int:pk>', views.CarListDetail.as_view()),
    # path('cars/free/',views.get_free_cars),
    # path('cars/view/',views.ViewedCarList.as_view()),
    # path('cars/view/<int:pk>', views.ViewedCarListDetail.as_view()),
    # path('cars/<int:pk>/book', views.to_book),

    # path('trip/', views.TripList.as_view()),
    # path('trip/trip_price', views.TripPriceList.as_view()),
    # path('trip/trip_price/<int:pk>', views.TripPriceListDetail.as_view()),
    # path('trip/start/<int:pk>', views.trip_start),
    # re_path('trip/(?P<pk>\d)/logs$', views.post_get_logs),
    # re_path('trip/(?P<pk>\d)/logs/(?P<pk_log>\d)', views.TripLogListDetail.as_view()),
    # path('trip/finish/', views.trip_finish),

]
