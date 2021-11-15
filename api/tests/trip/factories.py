import factory
from tests.trip.factories import TripPrice, Trip, TripLog
from trip.models import Cars


class TripPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cars

    car_class = factory.SubFactory(ClassFactory)
    level_consumption = 2
    mark = "Mercedes-Benz"
    reg_number = "MP31523"
    color = "w"
    year = 2000
    latitude = 55.0
    status = "free"
    longitude = 37.0


class CarsFactoryTest(factory.django.DjangoModelFactory):
    class Meta:
        model = Cars

    car_class = factory.SubFactory(ClassFactory)
    level_consumption = 2
    mark = "Mercedes-Benz"
    reg_number = "MP31523"
    color = "w"
    year = 2000
    latitude = 55.5
    status = "free"
    longitude = 37.0
