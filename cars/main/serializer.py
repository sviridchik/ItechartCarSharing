from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt import tokens

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,source = 'user.username')
    password = serializers.CharField(max_length=128,source = 'user.password')

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'email', 'dtp_times', 'username', 'password')

    def save(self, **kwargs):

        # user,created = User.objects.update_or_create(first_name = self.data['username'], email=self.data['email'],password=self.data['password'])
        # raise Exception(self.data)
        # try :
        #     User.objects.filter(username=self.data['username']).update(email = self.data['email'],password = self.data['password'])
        #     user = User.objects.get(username=self.data['username'])
        #
        # except User.DoesNotExist:
        # user = User.objects.create_user(self.data['username'], self.data['email'], self.data['password'])
        user,created = User.objects.update_or_create(username = self.data['username'],defaults={'username':self.data['username'],'email':self.data['email'],'password':self.data['password']})
        if not created:
            raise Exception(created)
        # user, created = User.objects.update_or_create(self.data['username'], self.data['email'])


        # raise Exception(user2,user)
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
            tokens.RefreshToken(self.token).blacklist()
        except exceptions.TokenError:
            self.fail('bad_token')
