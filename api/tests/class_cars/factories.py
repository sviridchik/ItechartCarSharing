import factory
from class_cars.models import ClassCar
from tests.price.factories import PriceFactory


class ClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClassCar

    price = factory.SubFactory(PriceFactory)
    name = "comfort",
    booking_time = 15
