from django.urls import path, include, re_path

from price import views

urlpatterns = [
    path('/', views.PriceList.as_view(), name='prices'),
    re_path('(?P<pk>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})',
            views.PriceListDetail.as_view(), name='price_pk'),
]
