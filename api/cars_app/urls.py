from django.urls import path, re_path

from . import views
from .utils import pk_reg

app_name = "cars"

urlpatterns = [

    path('/', views.CarList.as_view(), name='list'),
    re_path(pk_reg+'/$', views.CarListDetail.as_view(), name='detail'),
    path('/free/', views.FreeViewedCarsList.as_view(), name='free'),
    path('^/view/$', views.ViewedCarList.as_view(), name='view'),
    re_path('^/view/' + pk_reg + '$',
            views.ViewedCarListDetail.as_view(), name='view_pk'),
    re_path('/'+pk_reg+'/book', views.Booking.as_view()),

]
