import factory
from django.contrib.auth.models import User
from users.models import Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'test123'
    email = 'test@gmail.com'
    password = factory.PostGenerationMethodCall('set_password', 'test123123')


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        # permissions = (('MyPermissionAdmin','MyPermissionPkME'))

    user = factory.SubFactory(UserFactory)
    dtp_times = 9
    date_of_birth = '2003-09-09'
