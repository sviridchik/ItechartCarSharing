from django.urls import path, re_path

from . import views

urlpatterns = [

    path('/', views.CarList.as_view(), name='cars'),
    re_path('(?P<pk>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})',
            views.CarListDetail.as_view(), name='cars_pk'),

    path('/free/', views.get_free_cars, name='cars_free'),
    # path('/free/?latitude=<latitude>&longitude=<longitude>&distance =<distance>&class=<class>ordering= distance')

    path('/view/', views.ViewedCarList.as_view(), name='cars_view'),
    re_path('/view/(?P<pk>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})',
            views.ViewedCarListDetail.as_view(), name='cars_view_pk'),

]
