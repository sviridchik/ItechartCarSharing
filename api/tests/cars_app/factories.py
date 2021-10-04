import factory
from cars_app.models import Cars
from tests.class_cars.factories import ClassFactory


class CarsFactory(factory.django.DjangoModelFactory):
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
