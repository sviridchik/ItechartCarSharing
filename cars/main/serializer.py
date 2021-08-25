from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'email', 'dtp_times', 'username', 'password')

    def save(self, **kwargs):
        user = User.objects.create_user(self.data['username'], self.data['email'], self.data['password'])
        profile = Profile.objects.create(user=user, date_of_birth=self.data['date_of_birth'],
                                         email=self.data['email'],
                                         dtp_times=self.data['dtp_times'], )
        return profile


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
