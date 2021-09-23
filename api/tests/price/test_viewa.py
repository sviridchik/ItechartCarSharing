import uuid
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test.client import Client
from django.urls import reverse
from price.models import Price
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework_jwt.settings import api_settings
from users.models import Profile

from .factories import ProfileFactory,PriceFactory


# from price.views import ProfileList, ProfileDetailList


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


# ++++++++++++++++++++++ price +++++++++++++++++++++++++++++++++++++++++++++++
class NotAuth(APITestCase):
    def setUp(self):
        profile = ProfileFactory()

    def test_price_not_auth(self):
        response = self.client.post('/price/',
                                    data={
                                        "price_for_km": 23,
                                        "night_add": 13,
                                        "price_dtp": 8,
                                        "parking_price": 9,
                                        "booking_price": 23,
                                        "description": "very informative"
                                    })
        self.assertEqual(response.status_code, 401)

    def test_price_not_auth_get(self):
        price = PriceFactory()

        response = self.client.get('/price/')
        self.assertEqual(response.status_code, 401)

    def test_users_not_auth_get_pk(self):
        price = PriceFactory()
        response = self.client.get('/price/{}'.format(Price.objects.all()[0].id))
        self.assertEqual(response.status_code, 401)

class PricePostTest(PseudoAuth):

    def test_price(self):
        payload = {
            "price_for_km": 23,
            "night_add": 13,
            "price_dtp": 8,
            "parking_price": 9,
            "booking_price": 23,
            "description": "very informative"
        }

        Profile.objects.all().update(is_admin=True)
        response = self.client.post('/price/', data=payload)
        self.assertEqual(response.status_code, 201)

    # looks like worked permissions
    def test_price_not_admin(self):
        response = self.client.post('/price/',
                                    data={
                                        "price_for_km": 23,
                                        "night_add": 13,
                                        "price_dtp": 8,
                                        "parking_price": 9,
                                        "booking_price": 23,
                                        "description": "very informative"
                                    })
        self.assertEqual(response.status_code, 201)


class PriceGetTest(PseudoAuth):

    def test_price(self):
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        response = self.client.get('/price/')
        self.assertEqual(response.status_code, 200)

    def test_price_not_admin(self):
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        Profile.objects.all().update(is_admin=False)
        response = self.client.get('/price/')
        self.assertEqual(response.status_code, 403)

#
# #
# class PriceGetTestPk(PseudoAuth):
#
#     # def setUp(self):
#     #     self.user = self.client.post('/users/signup',
#     #                                  data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#     #                                        "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#     #
#     #     # raise Exception(Profile.objects.all()[0].is_admin)
#     #     response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#     #     self.token = response.data['access']
#     #
#     #     # self.api_authentication()
#     #
#     # def api_authentication(self):
#     #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_price(self):
#         # self.api_authentication()
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
#         id = Price.objects.all()[0].id
#         response = self.client.get('/price/{}'.format(id))
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         # self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         self.client.post('/price/',
#                          data={
#                              "price_for_km": 23,
#                              "night_add": 13,
#                              "price_dtp": 8,
#                              "parking_price": 9,
#                              "booking_price": 23,
#                              "description": "very informative"
#                          })
#         Profile.objects.all().update(is_admin=False)
#         id = Price.objects.all()[0].id
#         response = self.client.get('/price/{}'.format(id))
#         self.assertEqual(response.status_code, 200)
#


#
# class Price_patch_test_pk(APITestCase):
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
#         id = Price.objects.all()[0].id
#         response = self.client.patch('/price/{}'.format(id), data={"price_dtp": 3, })
#         self.assertEqual(Price.objects.get(pk=id).price_dtp, 3)
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
#         Profile.objects.all().update(is_admin=False)
#         id = Price.objects.all()[0].id
#         response = self.client.patch('/price/{}'.format(id), data={"price_dtp": 3, })
#         self.assertEqual(Price.objects.get(pk=id).price_dtp, 8)
#         self.assertEqual(response.status_code, 401)
#
#
# def test_users_not_auth(self):
#     response = self.client.patch('/price/{}'.format(id), data={})
#     self.assertEqual(response.status_code, 401)
#
#
# class Price_delete_test_pk(APITestCase):
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
#         id = Price.objects.all()[0].id
#         response = self.client.delete('/price/{}'.format(id))
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
#         Profile.objects.all().update(is_admin=False)
#         id = Price.objects.all()[0].id
#         response = self.client.delete('/price/{}'.format(id))
#         self.assertEqual(response.status_code, 401)
#
#     def test_users_not_auth(self):
#         response = self.client.delete('/price/{}'.format(1))
#         self.assertEqual(response.status_code, 401)
