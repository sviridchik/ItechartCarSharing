from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt import tokens

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, source='user.username')
    password = serializers.CharField(max_length=128, source='user.password')

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'email', 'dtp_times', 'username', 'password')

    def save(self, **kwargs):
        ps = make_password(self.data['password'])
        user, created = User.objects.update_or_create(username=self.data['username'],
                                                      defaults={'username': self.data['username'],
                                                                'email': self.data['email'], 'password': ps})

        profile = Profile.objects.update_or_create(user=user, date_of_birth=self.data['date_of_birth'],
                                                   email=self.data['email'],
                                                   dtp_times=self.data['dtp_times'],
                                                   defaults={'user': user, 'date_of_birth': self.data['date_of_birth'],
                                                             'email': self.data['email'],
                                                             'dtp_times': self.data['dtp_times']})
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
            tokens.RefreshToken(self.token).blacklist()
        except exceptions.TokenError:
            self.fail('bad_token')
