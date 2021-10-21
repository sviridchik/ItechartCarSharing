from cars.urls import pk_reg
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from users import views

# app_name = "users"

urlpatterns = [
    path('signin/', TokenObtainPairView.as_view(), name='signin'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('^/$', views.ProfileList.as_view(), name='users'),
    re_path('(?P<me>me)|' + pk_reg,
            views.ProfileDetailList.as_view(), name='users_pk'),

]
