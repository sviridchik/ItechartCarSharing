# import uuid
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User, Permission
# from django.contrib.contenttypes.models import ContentType
# from django.test.client import Client
# from django.urls import reverse
# from price.models import Price
# from rest_framework import status
# from rest_framework.test import APIRequestFactory
# from rest_framework.test import APITestCase
# from rest_framework.test import force_authenticate
# from rest_framework_jwt.settings import api_settings
# from users.models import Profile
#
# from .factories import ProfileFactory, PriceFactory
#
#
# class PseudoAuth(APITestCase):
#     def setUp(self):
#         profile = ProfileFactory()
#
#         ps = profile.user.password
#         self.user = profile.user
#
#         self.client.force_authenticate(self.user)
#         User.objects.filter(username=profile.user.username).update(password=make_password(ps))
#         permission = Permission.objects.all()
#         for p in permission:
#             self.user.user_permissions.add(p)
#         PriceFactory()
#
#
# # ++++++++++++++++++++++ price +++++++++++++++++++++++++++++++++++++++++++++++
# class NotAuth(APITestCase):
#     def setUp(self):
#         ProfileFactory()
#
#     def test_price_not_auth(self):
#         response = self.client.post(reverse('prices'),
#                                     data={
#                                         "price_for_km": 23,
#                                         "night_add": 13,
#                                         "price_dtp": 8,
#                                         "parking_price": 9,
#                                         "booking_price": 23,
#                                         "description": "very informative"
#                                     })
#         self.assertEqual(response.status_code, 401)
#
#     def test_price_not_auth_get(self):
#         PriceFactory()
#         response = self.client.get(reverse('prices'))
#         self.assertEqual(response.status_code, 401)
#
#     def test_users_not_auth_get_pk(self):
#         PriceFactory()
#         response = self.client.get('/price/{}'.format(Price.objects.all()[0].id))
#         self.assertEqual(response.status_code, 401)
#
#     def test_users_not_auth_patch(self):
#         PriceFactory()
#         response = self.client.patch('/price/{}'.format(Price.objects.all()[0].id), data={})
#         self.assertEqual(response.status_code, 401)
#
#     def test_users_not_auth(self):
#         PriceFactory()
#         response = self.client.delete('/price/{}'.format(Price.objects.all()[0].id))
#         self.assertEqual(response.status_code, 401)
#
#
# class PricePostTest(PseudoAuth):
#     payload = {
#         "price_for_km": 23,
#         "night_add": 13,
#         "price_dtp": 8,
#         "parking_price": 9,
#         "booking_price": 23,
#         "description": "very informative"
#     }
#
#     def test_price(self):
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.post(reverse('prices'), data=PricePostTest.payload)
#         self.assertEqual(response.status_code, 201)
#
#     # looks like worked permissions
#     def test_price_not_admin(self):
#         response = self.client.post(reverse('prices'),
#                                     data=PricePostTest.payload)
#         self.assertEqual(response.status_code, 201)
#
#
# class PriceGetTest(PseudoAuth):
#
#     def test_price(self):
#         Profile.objects.all().update(is_admin=True)
#
#         response = self.client.get(reverse('prices'))
#         self.assertEqual(response.status_code, 200)
#
#     def test_price_not_admin(self):
#         Profile.objects.all().update(is_admin=True)
#
#         Profile.objects.all().update(is_admin=False)
#         response = self.client.get(reverse('prices'))
#         self.assertEqual(response.status_code, 403)
#
#
# class PriceGetTestPk(PseudoAuth):
#
#     def test_price(self):
#         Profile.objects.all().update(is_admin=True)
#         id = Price.objects.all()[0].id
#         response = self.client.get(reverse('price_pk', kwargs={'pk': id}))
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         Profile.objects.all().update(is_admin=True)
#         Profile.objects.all().update(is_admin=False)
#         id = Price.objects.all()[0].id
#         response = self.client.get(reverse('price_pk', kwargs={'pk': id}))
#         self.assertEqual(response.status_code, 200)
#
#
# class PricePatchTestPk(PseudoAuth):
#
#     def test_price(self):
#         Profile.objects.all().update(is_admin=True)
#         id = Price.objects.all()[0].id
#         response = self.client.patch(reverse('price_pk', kwargs={'pk': id}), data={"price_dtp": 3, })
#         self.assertEqual(Price.objects.get(pk=id).price_dtp, 3)
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         Profile.objects.all().update(is_admin=False)
#         id = Price.objects.all()[0].id
#         response = self.client.patch(reverse('price_pk', kwargs={'pk': id}), data={"price_dtp": 3, })
#         self.assertEqual(Price.objects.get(pk=id).price_dtp, 8)
#         self.assertEqual(response.status_code, 403)
#
#
# class PriceDeleteTestPk(PseudoAuth):
#
#     def test_price(self):
#         Profile.objects.all().update(is_admin=True)
#         id = Price.objects.all()[0].id
#         response = self.client.delete(reverse('price_pk', kwargs={'pk': id}))
#         self.assertEqual(response.status_code, 204)
#
#     def test_users_not_admin(self):
#         Profile.objects.all().update(is_admin=False)
#         id = Price.objects.all()[0].id
#         response = self.client.delete(reverse('price_pk', kwargs={'pk': id}))
#         self.assertEqual(response.status_code, 403)
