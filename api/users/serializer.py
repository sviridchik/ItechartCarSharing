from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt import tokens

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, source='user.username')
    password = serializers.CharField(max_length=128, source='user.password')
    email = serializers.EmailField(max_length=128, source='user.email')

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'email', 'dtp_times', 'username', 'password')

    def create(self, validated_data):
        ps = make_password(validated_data.get('user')['password'])
        user, created = User.objects.get_or_create(
            username=validated_data.get('user')['username'],
            defaults={'username': validated_data.get('user')['username'],
                      'email': validated_data.get('user')['email'], 'password': ps})

        profile, created = Profile.objects.get_or_create(user=user, date_of_birth=validated_data.get('date_of_birth'),
                                                         dtp_times=validated_data.get('dtp_times'),
                                                         defaults={'user': user,
                                                                   'date_of_birth': validated_data.get('date_of_birth'),
                                                                   # 'email': validated_data.get('email'),
                                                                   'dtp_times': validated_data.get('dtp_times')})
        return profile

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            instance.user.email = validated_data['user'].get('email', instance.user.email)
            instance.user.username = validated_data['user'].get('username', instance.user.username)
        instance.user.password = validated_data.get('password', instance.user.password)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.dtp_times = validated_data.get('dtp_times', instance.dtp_times)

        return instance


class ProfileSerializerRedused(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, source='user.username')
    email = serializers.EmailField(max_length=128, source='user.email')

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, attrs):
        if not (list(self.initial_data.keys())[0] in list(
                dict(ProfileSerializerRedused.__dict__['_declared_fields']).keys())):

            raise serializers.ValidationError("there is no a such field")
        else:
            return attrs

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            instance.user.email = validated_data['user'].get('email', instance.user.email)
            instance.user.username = validated_data['user'].get('username', instance.user.username)
        return instance


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
