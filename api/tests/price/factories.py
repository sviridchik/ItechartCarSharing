import factory
from django.contrib.auth.models import User
from users.models import Profile
from price.models import Price

class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price

    price_for_km = 23
    night_add = 13
    price_dtp = 8
    parking_price =  9
    booking_price = 23
    description = "very informative"

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
