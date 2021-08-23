from django.test import TestCase
import datetime

from rest_framework.test import APITestCase
from .models import *
from main.models import Profile
from django.test import Client

req_test_health = {}
# Create your tests here.

# ++++++++++++++++++++++ price +++++++++++++++++++++++++++++++++++++++++++++++
class Price_post_test(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_price(self):
        payload = {
            "price_for_km": 23,
            "night_add": 13,
            "price_dtp": 8,
            "parking_price": 9,
            "booking_price": 23,
            "description": "very informative"
        }

        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        response = self.client.post('/price/', data=payload)
        self.assertEqual(response.status_code, 201)

    def test_price_not_admin(self):
        self.api_authentication()
        response = self.client.post('/price',
                                    data={
                                        "price_for_km": 23,
                                        "night_add": 13,
                                        "price_dtp": 8,
                                        "parking_price": 9,
                                        "booking_price": 23,
                                        "description": "very informative"
                                    })
        self.assertEqual(response.status_code, 401)

    def test_price_not_auth(self):
        response = self.client.post('/price',
                                    data={
                                        "price_for_km": 23,
                                        "night_add": 13,
                                        "price_dtp": 8,
                                        "parking_price": 9,
                                        "booking_price": 23,
                                        "description": "very informative"
                                    })
        self.assertEqual(response.status_code, 401)


#
class Price_get_test(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_price(self):
        self.api_authentication()
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
        response = self.client.get('/price')
        self.assertEqual(response.status_code, 200)

    def test_price_not_admin(self):
        self.api_authentication()
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
        self.assertEqual(response.status_code, 200)

    def test_price_not_auth(self):
        response = self.client.get('/price/')
        self.assertEqual(response.status_code, 401)


#
class Price_get_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_price(self):
        self.api_authentication()
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
        id = Price.objects.all()[0].id
        response = self.client.get('/price/{}'.format(id))
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
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
        id = Price.objects.all()[0].id
        response = self.client.get('/price/{}'.format(id))
        self.assertEqual(response.status_code, 200)

    def test_users_not_auth(self):
        response = self.client.get('/price/{}'.format(1))
        self.assertEqual(response.status_code, 401)


class Price_patch_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_price(self):
        self.api_authentication()
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
        id = Price.objects.all()[0].id
        response = self.client.patch('/price/{}'.format(id), data={"price_dtp": 3, })
        self.assertEqual(Price.objects.get(pk=id).price_dtp, 3)
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
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
        id = Price.objects.all()[0].id
        response = self.client.patch('/price/{}'.format(id), data={"price_dtp": 3, })
        self.assertEqual(Price.objects.get(pk=id).price_dtp, 8)
        self.assertEqual(response.status_code, 401)


class Price_delete_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_price(self):
        self.api_authentication()
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
        id = Price.objects.all()[0].id
        response = self.client.delete('/price/{}'.format(id))
        self.assertEqual(response.status_code, 204)

    def test_users_not_admin(self):
        self.api_authentication()
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
        id = Price.objects.all()[0].id
        response = self.client.delete('/price/{}'.format(id))
        self.assertEqual(response.status_code, 401)

    def test_users_not_auth(self):
        response = self.client.delete('/price/{}'.format(1))
        self.assertEqual(response.status_code, 401)

