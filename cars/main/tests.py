from rest_framework.test import APITestCase
from .models import *
from django.test import Client

req_test_health = {}


#
# class NoRightstest(APITestCase):
#
#     # 401 Unauthorized Error
#     def test_health(self):
#         response = self.client.get('/health')
#         self.assertEqual(response.status_code, 401)
#
#
# class My_Authtest(APITestCase):
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         self.api_authentication()
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_health(self):
#         response = self.client.get('/health')
#         self.assertEqual(response.status_code, 200)
#
#
# class Logouttest2(APITestCase):
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#         response = self.client.post('/auth/jwt/create/', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         response = self.client.post('users/logout', HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     # 401 Unauthorized Error
#     def test_health(self):
#         response = self.client.get('/health')
#         self.assertEqual(response.status_code, 401)
#
#
# class User_get_test(APITestCase):
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
#     def test_users(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.get('/users/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         # Profile.objects.all().update(is_admin=True)
#         response = self.client.get('/users/')
#         self.assertEqual(response.status_code, 401)
#
#     def test_users_not_auth(self):
#         response = self.client.get('/users/')
#         self.assertEqual(response.status_code, 401)
#
#
# class User_get_test_me(APITestCase):
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
#     def test_users(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         response = self.client.get('/users/me')
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         response = self.client.get('/users/me')
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_auth(self):
#         response = self.client.get('/users/me')
#         self.assertEqual(response.status_code, 401)
#
#
# class User_get_test_pk(APITestCase):
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
#     def test_users(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.get('/users/{}'.format(self.user_id))
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin_his_pk(self):
#         self.api_authentication()
#         response = self.client.get('/users/{}'.format(self.user_id))
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin_and_not_his_pk(self):
#         self.api_authentication()
#         response = self.client.get('/users/{}'.format(self.user_id + 1))
#         self.assertEqual(response.status_code, 401)
#
#     def test_users_not_auth(self):
#         response = self.client.get('/users/me')
#         self.assertEqual(response.status_code, 401)
#
#
# class User_patch_test_me(APITestCase):
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
#     def test_users(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         response = self.client.patch('/users/me', data={"email": "abracadabra@gmail.com"})
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         response = self.client.patch('/users/me', data={"email": "abracadabra@gmail.com"})
#         self.assertEqual(response.status_code, 200)
#
#     #
#     def test_users_not_auth(self):
#         response = self.client.patch('/users/me', data={"email": "abracadabra@gmail.com"})
#         self.assertEqual(response.status_code, 401)
#
#     def test_users_invalid_field(self):
#         self.api_authentication()
#         response = self.client.patch('/users/me', data={"parents": "abracadabra@gmail.com"})
#         self.assertEqual(response.status_code, 400)
#
#
# class User_patch_test_pk(APITestCase):
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
#     def test_users(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin_his_pk(self):
#         self.api_authentication()
#         response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin_and_not_his_pk(self):
#         self.api_authentication()
#         response = self.client.get('/users/{}'.format(self.user_id + 1), data={"email": "abracadabra@gmail.com"})
#         self.assertEqual(response.status_code, 401)
#
#     def test_users_not_auth(self):
#         response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
#         self.assertEqual(response.status_code, 401)
#
#
# class User_delete_test_me(APITestCase):
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
#     def test_users(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         response = self.client.delete('/users/me')
#
#         self.assertEqual(len(Profile.objects.all()), 0)
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         response = self.client.delete('/users/me')
#         self.assertEqual(len(Profile.objects.all()), 0)
#
#         self.assertEqual(response.status_code, 200)
#
#     # #
#     def test_users_not_auth(self):
#         response = self.client.delete('/users/me')
#         self.assertEqual(len(Profile.objects.all()), 1)
#         self.assertEqual(response.status_code, 401)
#
#
# class User_delete_test_pk(APITestCase):
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
#     def test_users(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         response = self.client.delete('/users/{}'.format(self.user_id))
#         self.assertEqual(len(Profile.objects.all()), 0)
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin_his_pk(self):
#         self.api_authentication()
#         response = self.client.delete('/users/{}'.format(self.user_id))
#         self.assertEqual(len(Profile.objects.all()), 0)
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin_and_not_his_pk(self):
#         self.api_authentication()
#         response = self.client.get('/users/{}'.format(self.user_id + 1))
#         self.assertEqual(len(Profile.objects.all()), 1)
#         self.assertEqual(response.status_code, 401)
#
#     def test_users_not_auth(self):
#         response = self.client.delete('/users/{}'.format(self.user_id))
#         self.assertEqual(len(Profile.objects.all()), 1)
#         self.assertEqual(response.status_code, 401)
#
#
# # ++++++++++++++++++++++ price +++++++++++++++++++++++++++++++++++++++++++++++
# class Price_post_test(APITestCase):
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
#         payload = {
#             "price_for_km": 23,
#             "night_add": 13,
#             "price_dtp": 8,
#             "parking_price": 9,
#             "booking_price": 23,
#             "description": "very informative"
#         }
#
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.post('/price/', data=payload)
#         self.assertEqual(response.status_code, 201)
#
#     def test_price_not_admin(self):
#         self.api_authentication()
#         response = self.client.post('/price',
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
#     def test_price_not_auth(self):
#         response = self.client.post('/price',
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
#
# #
# class Price_get_test(APITestCase):
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
#         response = self.client.get('/price/')
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
#         Profile.objects.all().update(is_admin=False)
#
#         response = self.client.get('/price/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_price_not_auth(self):
#         response = self.client.get('/price/')
#         self.assertEqual(response.status_code, 401)
#
#
# #
# class Price_get_test_pk(APITestCase):
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
#         id = Price.objects.all()[0].id
#         response = self.client.get('/price/{}'.format(id))
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
#         response = self.client.get('/price/{}'.format(id))
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_auth(self):
#         response = self.client.get('/price/{}'.format(1))
#         self.assertEqual(response.status_code, 401)
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
#
#
# # +++++++++++++++++++++++++++++++++++++++++ class ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# class Class_post_test(APITestCase):
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
#     def test_class(self):
#         payload = {
#             "price_for_km": 23,
#             "night_add": 13,
#             "price_dtp": 8,
#             "parking_price": 9,
#             "booking_price": 23,
#             "description": "very informative"
#         }
#
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.post('/price/', data=payload)
#
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         self.assertEqual(response.status_code, 201)
#
#     def test_price_not_admin(self):
#         self.api_authentication()
#         response = self.client.post('/price',
#                                     data={
#                                         "price_for_km": 23,
#                                         "night_add": 13,
#                                         "price_dtp": 8,
#                                         "parking_price": 9,
#                                         "booking_price": 23,
#                                         "description": "very informative"
#                                     })
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         self.assertEqual(response.status_code, 401)
#
#     #
#     def test_price_not_auth(self):
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         self.assertEqual(response.status_code, 401)
#
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
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         response = self.client.get('/class/')
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
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         Profile.objects.all().update(is_admin=False)
#
#         response = self.client.get('/class/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_price_not_auth(self):
#         response = self.client.get('/class/')
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
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         id = Class_car.objects.all()[0].id
#         response = self.client.get('/class/{}'.format(id))
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
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         Profile.objects.all().update(is_admin=False)
#
#         id = Class_car.objects.all()[0].id
#         response = self.client.get('/class/{}'.format(id))
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_auth(self):
#         response = self.client.get('/class/{}'.format(1))
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
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         id = Class_car.objects.all()[0].id
#         response = self.client.patch('/class/{}'.format(id), data={"booking_time": 21, })
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
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         Profile.objects.all().update(is_admin=False)
#         id = Class_car.objects.all()[0].id
#         response = self.client.patch('/class/{}'.format(id), data={"booking_time": 21, })
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
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         id = Class_car.objects.all()[0].id
#         response = self.client.delete('/class/{}'.format(id))
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
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         Profile.objects.all().update(is_admin=False)
#         id = Class_car.objects.all()[0].id
#         response = self.client.delete('/class/{}'.format(id))
#         self.assertEqual(response.status_code, 401)
#
#
# #
#
#
# # ---------------------------  cars ---------------------------------------------------
# class Car_post_test(APITestCase):
#     payload_car = {
#         "level_consumption": 2,
#         "mark": "Mercedes-Benz",
#         "reg_number": "MP31523",
#         "color": "w",
#         "year": 2000,
#         "latitude": 55.0,
#         "status": "active",
#         "car_class": 1,
#         "longitude": 37.0}
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         # self.api_authentication()
#         payload = {
#             "price_for_km": 23,
#             "night_add": 13,
#             "price_dtp": 8,
#             "parking_price": 9,
#             "booking_price": 23,
#             "description": "very informative"
#         }
#
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.post('/price/', data=payload)
#
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         Profile.objects.all().update(is_admin=False)
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_car(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         #
#         response = self.client.post('/cars/', data=Car_post_test.payload_car)
#         # raise Exception(Price.objects.all()[0].description)
#         self.assertEqual(response.status_code, 201)
#
#     def test_price_not_admin(self):
#         self.api_authentication()
#
#         response = self.client.post('/cars/', data=Car_post_test.payload_car)
#         self.assertEqual(response.status_code, 401)
#
#     def test_price_not_auth(self):
#         response = self.client.post('/cars/', data=Car_post_test.payload_car)
#         self.assertEqual(response.status_code, 401)
#
#
# #
# class Car_get_test(APITestCase):
#     payload_car = {
#         "level_consumption": 2,
#         "mark": "Mercedes-Benz",
#         "reg_number": "MP31523",
#         "color": "w",
#         "year": 2000,
#         "latitude": 55.0,
#         "status": "active",
#         "car_class": 1,
#         "longitude": 37.0}
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         payload = {
#             "price_for_km": 23,
#             "night_add": 13,
#             "price_dtp": 8,
#             "parking_price": 9,
#             "booking_price": 23,
#             "description": "very informative"
#         }
#
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.post('/price/', data=payload)
#
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         response = self.client.post('/cars/', data=Car_get_test.payload_car)
#
#         Profile.objects.all().update(is_admin=False)
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_cars(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         response = self.client.get('/cars/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_cars_not_admin(self):
#         self.api_authentication()
#         response = self.client.get('/cars/')
#         self.assertEqual(response.status_code, 200)
#
#
# class Car_get_test_pk(APITestCase):
#     payload_car = {
#         "level_consumption": 2,
#         "mark": "Mercedes-Benz",
#         "reg_number": "MP31523",
#         "color": "w",
#         "year": 2000,
#         "latitude": 55.0,
#         "status": "active",
#         "car_class": 1,
#         "longitude": 37.0}
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         payload = {
#             "price_for_km": 23,
#             "night_add": 13,
#             "price_dtp": 8,
#             "parking_price": 9,
#             "booking_price": 23,
#             "description": "very informative"
#         }
#
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.post('/price/', data=payload)
#
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         response = self.client.post('/cars/', data=Car_get_test_pk.payload_car)
#
#         Profile.objects.all().update(is_admin=False)
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_price(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         id = Cars.objects.all()[0].id
#         response = self.client.get('/cars/{}'.format(id))
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         id = Cars.objects.all()[0].id
#         response = self.client.get('/cars/{}'.format(id))
#         self.assertEqual(response.status_code, 200)
#
#
# class Car_patch_test_pk(APITestCase):
#     payload_car = {
#         "level_consumption": 2,
#         "mark": "Mercedes-Benz",
#         "reg_number": "MP31523",
#         "color": "w",
#         "year": 2000,
#         "latitude": 55.0,
#         "status": "active",
#         "car_class": 1,
#         "longitude": 37.0}
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         # self.api_authentication()
#         payload = {
#             "price_for_km": 23,
#             "night_add": 13,
#             "price_dtp": 8,
#             "parking_price": 9,
#             "booking_price": 23,
#             "description": "very informative"
#         }
#
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.post('/price/', data=payload)
#
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         response = self.client.post('/cars/', data=Car_patch_test_pk.payload_car)
#
#         Profile.objects.all().update(is_admin=False)
#
#     def test_cars(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         id = Cars.objects.all()[0].id
#         response = self.client.patch('/cars/{}'.format(id), data={"level_consumption": 10, })
#         self.assertEqual(Cars.objects.get(pk=id).level_consumption, 10)
#         self.assertEqual(response.status_code, 200)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         Profile.objects.all().update(is_admin=False)
#         id = Class_car.objects.all()[0].id
#         response = self.client.patch('/class/{}'.format(id), data={"level_consumption": 10, })
#         self.assertEqual(Cars.objects.get(pk=id).level_consumption, 2)
#         self.assertEqual(response.status_code, 401)
#
#
# class Car_delete_test_pk(APITestCase):
#     payload_car = {
#         "level_consumption": 2,
#         "mark": "Mercedes-Benz",
#         "reg_number": "MP31523",
#         "color": "w",
#         "year": 2000,
#         "latitude": 55.0,
#         "status": "active",
#         "car_class": 1,
#         "longitude": 37.0}
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         payload = {
#             "price_for_km": 23,
#             "night_add": 13,
#             "price_dtp": 8,
#             "parking_price": 9,
#             "booking_price": 23,
#             "description": "very informative"
#         }
#
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.post('/price/', data=payload)
#
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "comfort",
#             "price": 1,
#             "booking_time": 15
#         })
#         response = self.client.post('/cars/', data=Car_delete_test_pk.payload_car)
#
#         Profile.objects.all().update(is_admin=False)
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_price(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         id = Cars.objects.all()[0].id
#         response = self.client.delete('/cars/{}'.format(id))
#         self.assertEqual(response.status_code, 204)
#
#     def test_users_not_admin(self):
#         self.api_authentication()
#         id = Cars.objects.all()[0].id
#         response = self.client.delete('/cars/{}'.format(id))
#         self.assertEqual(response.status_code, 401)
# #
# # ========== viewed cars free ===========
#
#
# class Car_free_get_test(APITestCase):
#     payload_car = {
#         "level_consumption": 2,
#         "mark": "Mercedes-Benz",
#         "reg_number": "MP31523",
#         "color": "w",
#         "year": 2000,
#         "latitude": 55.0,
#         "status": "free",
#         "car_class": 1,
#         "longitude": 37.0}
#
#     def setUp(self):
#         self.user = self.client.post('/users/signup',
#                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#
#         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#         self.token = response.data['access']
#         payload = {
#             "price_for_km": 23,
#             "night_add": 13,
#             "price_dtp": 8,
#             "parking_price": 9,
#             "booking_price": 23,
#             "description": "very informative"
#         }
#
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.post('/price/', data=payload)
#
#         response = self.client.post('/class/', data={
#             "id": 1,
#             "name": "economy",
#             "price": 1,
#             "booking_time": 15
#         })
#         response = self.client.post('/cars/', data=Car_get_test.payload_car)
#
#         Profile.objects.all().update(is_admin=False)
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_cars(self):
#         self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         response = self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class=economy&ordering=distance')
#         self.assertEqual(response.status_code, 200)
#
#     def test_cars_not_admin(self):
#         self.api_authentication()
#         response = self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class=economy&ordering=distance')
#         self.assertEqual(response.status_code, 200)
#
#


class Car_book_test(APITestCase):
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

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
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

        response = self.client.post('/class/', data={
            "id": 1,
            "name": "economy",
            "price": 1,
            "booking_time": 15
        })
        response = self.client.post('/cars/', data=Car_book_test.payload_car)

        Profile.objects.all().update(is_admin=False)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_cars(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class=economy&ordering=distance')

        id_car = ViewedCars.objects.all()[0].id
        response1 = self.client.post('/cars/{}/book'.format(id_car))

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(Cars.objects.get(pk=id_car).status, "active")
        self.assertNotEqual(len(TripPrice.objects.all()), 0)
        self.assertNotEqual(len(TripLog.objects.all()), 0)
        self.assertEqual(len(ViewedCars.objects.all()), 0)
