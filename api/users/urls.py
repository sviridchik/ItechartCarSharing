from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from users import views

urlpatterns = [
    path('signin/', TokenObtainPairView.as_view(), name='signin'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('/', views.ProfileList.as_view(), name='users'),
    re_path('(?P<me>me)|(?P<pk>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})', views.ProfileDetailList.as_view(), name='users_me'),
]
