from cars_app.models import Cars, ViewedCars
from class_cars.models import ClassCar
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tests.users.factories import ProfileFactory
from trip.models import TripPrice, Trip, TripLog
from users.models import Profile

from .factories import CarsFactory


class NotAuthCarsTest(APITestCase):
    def setUp(self):
        ProfileFactory()
        CarsFactory()

    def test_price_not_auth(self):
        response = self.client.post(reverse('cars'), data=CarPostTest.payload_car)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_not_admin(self):
        id = Cars.objects.all()[0].id
        response = self.client.patch('/class/{}'.format(id), data={"level_consumption": 10, })
        self.assertEqual(Cars.objects.get(pk=id).level_consumption, 2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


#
class PseudoAuth(APITestCase):
    def setUp(self):
        profile = ProfileFactory()
        ps = profile.user.password
        self.user = profile.user

        self.client.force_authenticate(self.user)
        User.objects.filter(username=profile.user.username).update(password=make_password(ps))
        permission = Permission.objects.all()
        # for p in permission:
        #     self.user.user_permissions.add(p)
        CarsFactory()


class CarPostTest(PseudoAuth):
    payload_car = {
        "level_consumption": 2,
        "mark": "Mercedes-Benz",
        "reg_number": "MP31523",
        "color": "w",
        "year": 2000,
        "latitude": 55.0,
        "status": "active",
        "longitude": 37.0}

    def test_car(self):
        Profile.objects.all().update(is_admin=True)
        id = ClassCar.objects.all()[0].id
        CarPostTest.payload_car["car_class"] = id
        response = self.client.post(reverse('cars'), data=CarPostTest.payload_car)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_price_not_admin(self):
        id = ClassCar.objects.all()[0].id
        CarPostTest.payload_car["car_class"] = id
        response = self.client.post(reverse('cars'), data=CarPostTest.payload_car)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CarGetTest(PseudoAuth):
    payload_car = {
        "level_consumption": 2,
        "mark": "Mercedes-Benz",
        "reg_number": "MP31523",
        "color": "w",
        "year": 2000,
        "latitude": 55.0,
        "status": "active",
        "longitude": 37.0}

    def test_cars(self):
        id = ClassCar.objects.all()[0].id
        CarPostTest.payload_car["car_class"] = id
        Profile.objects.all().update(is_admin=True)
        response = self.client.get(reverse('cars'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cars_not_admin(self):
        id = ClassCar.objects.all()[0].id
        CarPostTest.payload_car["car_class"] = id
        response = self.client.get(reverse('cars'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CarGetTestPk(PseudoAuth):

    def test_price(self):
        Profile.objects.all().update(is_admin=True)
        id = Cars.objects.all()[0].id
        response = self.client.get('/cars/{}'.format(id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin(self):
        id = Cars.objects.all()[0].id
        response = self.client.get('/cars/{}'.format(id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CarPatchTestPk(PseudoAuth):

    def test_cars(self):
        Profile.objects.all().update(is_admin=True)
        id = Cars.objects.all()[0].id
        response = self.client.patch('/cars/{}'.format(id), data={"level_consumption": 10, })
        self.assertEqual(Cars.objects.get(pk=id).level_consumption, 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CarDeleteTestPk(PseudoAuth):

    def test_price(self):
        Profile.objects.all().update(is_admin=True)
        id = Cars.objects.all()[0].id
        response = self.client.delete('/cars/{}'.format(id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_not_admin(self):
        id = Cars.objects.all()[0].id
        response = self.client.delete('/cars/{}'.format(id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ========== viewed cars free ===========


class CarFreeGetTest(PseudoAuth):

    def test_cars(self):
        CarsFactory()
        CarsFactory()
        Profile.objects.all().update(is_admin=True)
        response = self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class=comfort&ordering=distance')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(ViewedCars.objects.all()), 3)

    #
    def test_cars_not_admin(self):
        CarsFactory()
        CarsFactory()
        response = self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class=economy&ordering=distance')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(ViewedCars.objects.all()), 0)


#         book

class Car_book_test(PseudoAuth):
    payload_car = {
        "level_consumption": 2,
        "mark": "Mercedes-Benz",
        "reg_number": "MP31523",
        "color": "w",
        "year": 2000,
        "latitude": 55.0,
        "status": "free",
        "car_class": 1,
        "longitude": 37.0}

    def test_cars(self):
        Profile.objects.all().update(is_admin=True)

        self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class=comfort&ordering=distance')

        id_car = ViewedCars.objects.all()[0].car.id
        response1 = self.client.post('/cars/{}/book'.format(id_car))

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(Cars.objects.get(pk=id_car).status, "booked")
        self.assertNotEqual(len(TripPrice.objects.all()), 0)
        self.assertNotEqual(len(TripLog.objects.all()), 0)
        self.assertEqual(len(ViewedCars.objects.all()), 0)
