from cars.urls import pk_reg
from django.urls import path, re_path
from price import views
app_name = "price"

urlpatterns = [
    path('/', views.PriceList.as_view(), name='list'),
    re_path(pk_reg,
            views.PriceListDetail.as_view(), name='pk'),
]
