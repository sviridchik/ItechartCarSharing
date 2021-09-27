from django.test import TestCase
from django.test import TestCase
import datetime
from users.models import Profile
from django.contrib.auth.models import User, Permission
from rest_framework.test import APITestCase
from class_cars.models import *
from django.test import Client
from tests.users.factories import ProfileFactory
from tests.price.factories import PriceFactory

from django.contrib.auth.hashers import make_password

class PseudoAuth(APITestCase):
    def setUp(self):
        profile = ProfileFactory()
        ps = profile.user.password
        self.user = profile.user

        self.client.force_authenticate(self.user)
        User.objects.filter(username=profile.user.username).update(password=make_password(ps))
        permission = Permission.objects.all()
        for p in permission:
            self.user.user_permissions.add(p)
        PriceFactory()
# +++++++++++++++++++++++++++++++++++++++++ class_cars ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Class_post_test(PseudoAuth):

    # def setUp(self):
        # self.user = self.client.post('/users/signup',
        #                              data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
        #                                    "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
        #
        # response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        # self.token = response.data['access']

    # def api_authentication(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_class(self):
        # payload = {
        #     "price_for_km": 23,
        #     "night_add": 13,
        #     "price_dtp": 8,
        #     "parking_price": 9,
        #     "booking_price": 23,
        #     "description": "very informative"
        # }

        # self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        # response = self.client.post('/price/', data=payload)

        response = self.client.post('/class_cars/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        self.assertEqual(response.status_code, 201)

    def test_price_not_admin(self):
        # self.api_authentication()
        response = self.client.post('/price',
                                    data={
                                        "price_for_km": 23,
                                        "night_add": 13,
                                        "price_dtp": 8,
                                        "parking_price": 9,
                                        "booking_price": 23,
                                        "description": "very informative"
                                    })
        response = self.client.post('/class_cars/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        self.assertEqual(response.status_code, 401)

    #
    def test_price_not_auth(self):
        response = self.client.post('/class_cars/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        self.assertEqual(response.status_code, 401)

#
# class Class_get_test(APITestCase):
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_price(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         self.client.post('/price',
#                          data={
#                              "price_for_km": 23,
#                              "night_add": 13,
#                              "price_dtp": 8,
#                              "parking_price": 9,
#                              "booking_price": 23,
#                              "description": "very informative"
#                          })
#         response = self.client.post('/class_cars/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         response = self.client.get('/class_cars/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_price_not_admin(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         self.client.post('/price',
#                          data={
#                              "price_for_km": 23,
#                              "night_add": 13,
#                              "price_dtp": 8,
#                              "parking_price": 9,
#                              "booking_price": 23,
#                              "description": "very informative"
#                          })
#         response = self.client.post('/class_cars/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         Profile.objects.all().update(is_admin=False)
#
#         response = self.client.get('/class_cars/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_price_not_auth(self):
#         response = self.client.get('/class_cars/')
#         self.assertEqual(response.status_code, 401)
#
#
# class Class_get_test_pk(APITestCase):
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_price(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         self.client.post('/price',
#                          data={
#                              "price_for_km": 23,
#                              "night_add": 13,
#                              "price_dtp": 8,
#                              "parking_price": 9,
#                              "booking_price": 23,
#                              "description": "very informative"
#                          })
#         response = self.client.post('/class_cars/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         id = Class_car.objects.all()[0].id
#         response = self.client.get('/class_cars/{}'.format(id))
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         self.client.post('/price',
#                          data={
#                              "price_for_km": 23,
#                              "night_add": 13,
#                              "price_dtp": 8,
#                              "parking_price": 9,
#                              "booking_price": 23,
#                              "description": "very informative"
#                          })
#
#         response = self.client.post('/class_cars/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         Profile.objects.all().update(is_admin=False)
#
#         id = Class_car.objects.all()[0].id
#         response = self.client.get('/class_cars/{}'.format(id))
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_auth(self):
#         response = self.client.get('/class_cars/{}'.format(1))
#         self.assertEqual(response.status_code, 401)
#
#
# class Class_patch_test_pk(APITestCase):
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         self.user_id = Profile.objects.all()[0].id
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_price(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         self.client.post('/price',
#                          data={
#                              "price_for_km": 23,
#                              "night_add": 13,
#                              "price_dtp": 8,
#                              "parking_price": 9,
#                              "booking_price": 23,
#                              "description": "very informative"
#                          })
#         response = self.client.post('/class_cars/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         id = Class_car.objects.all()[0].id
#         response = self.client.patch('/class_cars/{}'.format(id), data={"booking_time": 21, })
#         self.assertEqual(Class_car.objects.get(pk=id).booking_time, 21)
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         self.client.post('/price',
#                          data={
#                              "price_for_km": 23,
#                              "night_add": 13,
#                              "price_dtp": 8,
#                              "parking_price": 9,
#                              "booking_price": 23,
#                              "description": "very informative"
#                          })
#         response = self.client.post('/class_cars/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         Profile.objects.all().update(is_admin=False)
#         id = Class_car.objects.all()[0].id
#         response = self.client.patch('/class_cars/{}'.format(id), data={"booking_time": 21, })
#         self.assertEqual(Class_car.objects.get(pk=id).booking_time, 15)
#         self.assertEqual(response.status_code, 401)
#
#
# class Class_delete_test_pk(APITestCase):
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         self.user_id = Profile.objects.all()[0].id
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_price(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         self.client.post('/price',
#                          data={
#                              "price_for_km": 23,
#                              "night_add": 13,
#                              "price_dtp": 8,
#                              "parking_price": 9,
#                              "booking_price": 23,
#                              "description": "very informative"
#                          })
#         response = self.client.post('/class_cars/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         id = Class_car.objects.all()[0].id
#         response = self.client.delete('/class_cars/{}'.format(id))
#         # raise Exception(Class_car.objects.all())
#
#         self.assertEqual(response.status_code, 204)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         self.client.post('/price',
#                          data={
#                              "price_for_km": 23,
#                              "night_add": 13,
#                              "price_dtp": 8,
#                              "parking_price": 9,
#                              "booking_price": 23,
#                              "description": "very informative"
#                          })
#         response = self.client.post('/class_cars/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         Profile.objects.all().update(is_admin=False)
#         id = Class_car.objects.all()[0].id
#         response = self.client.delete('/class_cars/{}'.format(id))
#         self.assertEqual(response.status_code, 401)
#
