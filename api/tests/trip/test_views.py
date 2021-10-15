# import datetime
# import uuid
# from cars_app.models import *
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User, Permission
# # from .models import *
# from django.test import Client
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APITestCase
# # Create your tests here.
# # from main.models import Profile
# from tests.users.factories import ProfileFactory
# from tests.cars_app.factories import CarsFactory
#
#
# class PseudoAuth(APITestCase):
#     def setUp(self):
#         profile = ProfileFactory()
#         ps = profile.user.password
#         self.user = profile.user
#         self.client.force_authenticate(self.user)
#         User.objects.filter(username=profile.user.username).update(password=make_password(ps))
#         permission = Permission.objects.all()
#         for p in permission:
#             self.user.user_permissions.add(p)
#         CarsFactory()
#
#
# class Trip_start_test(PseudoAuth):
#     # payload_car = {
#     #     "level_consumption": 2,
#     #     "mark": "Mercedes-Benz",
#     #     "reg_number": "MP31523",
#     #     "color": "w",
#     #     "year": 2000,
#     #     "latitude": 55.0,
#     #     "status": "free",
#     #     "car_class": 1,
#     #     "longitude": 37.0}
#     #
#     # def setUp(self):
#     #     self.user = self.client.post('/users/signup',
#     #                                  data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
#     #                                        "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
#     #
#     #     response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
#     #     self.token = response.data['access']
#     #     payload = {
#     #         "price_for_km": 23,
#     #         "night_add": 13,
#     #         "price_dtp": 8,
#     #         "parking_price": 9,
#     #         "booking_price": 23,
#     #         "description": "very informative"
#     #     }
#     #
#     #     self.api_authentication()
#     #     Profile.objects.all().update(is_admin=True)
#     #     self.client.post('/price/', data=payload)
#     #
#     #     self.client.post('/class_car/', data={
#     #         "id": 1,
#     #         "name": "economy",
#     #         "price": 1,
#     #         "booking_time": 15
#     #     })
#     #     self.client.post('/cars/', data=Trip_start_test.payload_car)
#     #
#     #     Profile.objects.all().update(is_admin=False)
#     #
#     # def api_authentication(self):
#     #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_cars_booked(self):
#         # self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
#
#         id_car = ViewedCars.objects.all()[0].id
#         self.client.post('/cars/{}/book'.format(id_car))
#         response2 = self.client.post('/trip/start/{}'.format(id_car))
#
#         self.assertEqual(response2.status_code, 200)
#         self.assertEqual(Cars.objects.get(pk=id_car).status, "active")
#         self.assertNotEqual(len(TripPrice.objects.all()), 0)
#         self.assertNotEqual(len(TripLog.objects.all()), 0)
#         self.assertEqual(len(ViewedCars.objects.all()), 0)
#
#     def test_cars_not_booked(self):
#         # self.api_authentication()
#         Profile.objects.all().update(is_admin=True)
#
#         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
#
#         id_car = ViewedCars.objects.all()[0].id
#         response2 = self.client.post('/trip/start/{}'.format(id_car))
#
#         self.assertEqual(response2.status_code, 200)
#         self.assertEqual(Cars.objects.get(pk=id_car).status, "active")
#         self.assertNotEqual(len(TripPrice.objects.all()), 0)
#         self.assertNotEqual(len(TripLog.objects.all()), 0)
#         self.assertEqual(len(ViewedCars.objects.all()), 0)
#
# #
# # class Logs_test(APITestCase):
# #     payload_car = {
# #         "level_consumption": 2,
# #         "mark": "Mercedes-Benz",
# #         "reg_number": "MP31523",
# #         "color": "w",
# #         "year": 2000,
# #         "latitude": 55.0,
# #         "status": "free",
# #         "car_class": 1,
# #         "longitude": 37.0}
# #
# #     def setUp(self):
# #         self.user = self.client.post('/users/signup',
# #                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
# #                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
# #
# #         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
# #         self.token = response.data['access']
# #         payload = {
# #             "price_for_km": 23,
# #             "night_add": 13,
# #             "price_dtp": 8,
# #             "parking_price": 9,
# #             "booking_price": 23,
# #             "description": "very informative"
# #         }
# #
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #         response = self.client.post('/price/', data=payload)
# #
# #         response = self.client.post('/class_car/', data={
# #             "id": 1,
# #             "name": "economy",
# #             "price": 1,
# #             "booking_time": 15
# #         })
# #         response = self.client.post('/cars/', data=Trip_start_test.payload_car)
# #
# #         Profile.objects.all().update(is_admin=False)
# #
# #     def api_authentication(self):
# #         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
# #
# #     def test_logs_post_get(self):
# #
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #
# #         response = self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         response1 = self.client.post('/cars/{}/book'.format(id_car))
# #         response2 = self.client.post('/trip/start/{}'.format(id_car))
# #         # raise Exception(Trip.objects.all()[0].is_active)
# #
# #         id_trip = Trip.objects.filter(is_active = True)[0].id
# #         # raise Exception(type(id_trip))
# #         now = datetime.datetime.now()
# #
# #         data_log = {'time_stamp': now.strftime("%H:%M"),
# #                     'type': 'active'
# #                     }
# #
# #         # raise Exception(id_trip)
# #         response = self.client.post('/trip/{}/logs'.format(id_trip),data=data_log)
# #         response2 = self.client.get('/trip/{}/logs'.format(id_trip))
# #
# #         # raise Exception(response)
# #         self.assertEqual(response.status_code, 201)
# #         self.assertEqual(response2.status_code, 200)
# #
# #
# #         self.assertEqual(Cars.objects.get(pk=id_car).status, "active")
# #         self.assertNotEqual(len(TripPrice.objects.all()), 0)
# #         self.assertNotEqual(len(TripLog.objects.all()), 0)
# #         self.assertEqual(len(ViewedCars.objects.all()), 0)
# #
# #
# #
# #     def test_cars_not_booked(self):
# #         log_choose = (
# #             ("active", "active"),
# #             ("finished", "finished"),
# #             ("booked", "booked"),
# #             ("stop", "stop"),
# #             ("start", "start"),
# #         )
# #
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #
# #         response = self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         response2 = self.client.post('/trip/start/{}'.format(id_car))
# #         id_trip = Trip.objects.filter(is_active=True)[0].id
# #         data_log = {}
# #         data_log['type'] = 'active'
# #
# #         # raise Exception(id_trip)
# #         response = self.client.post('/trip/{}/logs'.format(id_trip), data=data_log)
# #         response2 = self.client.get('/trip/{}/logs'.format(id_trip))
# #         self.assertEqual(response.status_code, 201)
# #         self.assertEqual(response2.status_code, 200)
# #         self.assertEqual(Cars.objects.get(pk=id_car).status, "active")
# #         self.assertNotEqual(len(TripPrice.objects.all()), 0)
# #         self.assertNotEqual(len(TripLog.objects.all()), 0)
# #         self.assertEqual(len(ViewedCars.objects.all()), 0)
# #
# #
# #
# #
# # class Trip_finish_test(APITestCase):
# #     payload_car = {
# #         "level_consumption": 2,
# #         "mark": "Mercedes-Benz",
# #         "reg_number": "MP31523",
# #         "color": "w",
# #         "year": 2000,
# #         "latitude": 55.0,
# #         "status": "free",
# #         "car_class": 1,
# #         "longitude": 37.0}
# #
# #     def setUp(self):
# #         self.user = self.client.post('/users/signup',
# #                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
# #                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
# #
# #         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
# #         self.token = response.data['access']
# #         payload = {
# #             "price_for_km": 23,
# #             "night_add": 13,
# #             "price_dtp": 8,
# #             "parking_price": 9,
# #             "booking_price": 23,
# #             "description": "very informative"
# #         }
# #
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #         self.client.post('/price/', data=payload)
# #
# #         self.client.post('/class_car/', data={
# #             "id": 1,
# #             "name": "economy",
# #             "price": 1,
# #             "booking_time": 15
# #         })
# #         self.client.post('/cars/', data=Trip_start_test.payload_car)
# #
# #         Profile.objects.all().update(is_admin=False)
# #
# #     def api_authentication(self):
# #         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
# #
# #     def test_trip_finish_get(self):
# #
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         id_trip = Trip.objects.filter(is_active = True)[0].id
# #         now = datetime.datetime.now()
# #
# #         data_log = {'time_stamp': now.strftime("%H:%M"),
# #                     'type': 'start'
# #                     }
# #
# #         self.client.post('/trip/{}/logs'.format(id_trip),data=data_log)
# #         self.client.get('/trip/{}/logs'.format(id_trip))
# #
# #
# #         response = self.client.post('/trip/finish/?latitude=53&longitude=37'.format(id_trip))
# #
# #         self.assertEqual(response.status_code, 201)
# #         self.assertNotEqual(Trip.objects.get(pk=id_trip).final_price, 0)
# #         self.assertEqual(Trip.objects.get(pk=id_trip).is_active, False)
# #         self.assertEqual(Cars.objects.get(pk=id_car).status, "free")
# #         self.assertEqual(TripLog.objects.latest('id').type, "finished")
# #
# #
# #
# #
# # class Trip_get_test_me(APITestCase):
# #     payload_car = {
# #         "level_consumption": 2,
# #         "mark": "Mercedes-Benz",
# #         "reg_number": "MP31523",
# #         "color": "w",
# #         "year": 2000,
# #         "latitude": 55.0,
# #         "status": "free",
# #         "car_class": 1,
# #         "longitude": 37.0}
# #
# #     def setUp(self):
# #         self.user = self.client.post('/users/signup',
# #                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
# #                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
# #
# #         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
# #         self.token = response.data['access']
# #         payload = {
# #             "price_for_km": 23,
# #             "night_add": 13,
# #             "price_dtp": 8,
# #             "parking_price": 9,
# #             "booking_price": 23,
# #             "description": "very informative"
# #         }
# #
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #         self.client.post('/price/', data=payload)
# #
# #         self.client.post('/class_car/', data={
# #             "id": 1,
# #             "name": "economy",
# #             "price": 1,
# #             "booking_time": 15
# #         })
# #         self.client.post('/cars/', data=Trip_get_test_me.payload_car)
# #
# #         Profile.objects.all().update(is_admin=False)
# #
# #     def api_authentication(self):
# #         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
# #
# #     def test_users(self):
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/me/trip/current')
# #         self.assertEqual(response.status_code, 200)
# #
# #     def test_users_not_admin(self):
# #         self.api_authentication()
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/me/trip/current')
# #         self.assertEqual(response.status_code, 200)
# #
# #
# #
# # class Trip_get_test_pk(APITestCase):
# #
# #     def setUp(self):
# #         self.user = self.client.post('/users/signup',
# #                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
# #                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
# #
# #         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
# #         self.token = response.data['access']
# #         payload = {
# #             "price_for_km": 23,
# #             "night_add": 13,
# #             "price_dtp": 8,
# #             "parking_price": 9,
# #             "booking_price": 23,
# #             "description": "very informative"
# #         }
# #
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #         self.client.post('/price/', data=payload)
# #
# #         self.client.post('/class_car/', data={
# #             "id": 1,
# #             "name": "economy",
# #             "price": 1,
# #             "booking_time": 15
# #         })
# #         self.client.post('/cars/', data=Trip_get_test_me.payload_car)
# #
# #         Profile.objects.all().update(is_admin=False)
# #         self.user_id = Profile.objects.all()[0].id
# #     def api_authentication(self):
# #         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
# #
# #     def test_users(self):
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/{}/trip/current'.format(self.user_id))
# #         self.assertEqual(response.status_code, 200)
# #
# #     def test_users_not_admin_his_pk(self):
# #         self.api_authentication()
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/{}/trip/current'.format(self.user_id))
# #         self.assertEqual(response.status_code, 200)
# #
# #     def test_users_not_admin_and_not_his_pk(self):
# #         self.api_authentication()
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/{}/trip/current'.format(self.user_id+1))
# #         self.assertEqual(response.status_code, 401)
# #
# #
# # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# #
# # class Trip_get_not_current_test_me(APITestCase):
# #     payload_car = {
# #         "level_consumption": 2,
# #         "mark": "Mercedes-Benz",
# #         "reg_number": "MP31523",
# #         "color": "w",
# #         "year": 2000,
# #         "latitude": 55.0,
# #         "status": "free",
# #         "car_class": 1,
# #         "longitude": 37.0}
# #
# #     def setUp(self):
# #         self.user = self.client.post('/users/signup',
# #                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
# #                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
# #
# #         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
# #         self.token = response.data['access']
# #         payload = {
# #             "price_for_km": 23,
# #             "night_add": 13,
# #             "price_dtp": 8,
# #             "parking_price": 9,
# #             "booking_price": 23,
# #             "description": "very informative"
# #         }
# #
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #         self.client.post('/price/', data=payload)
# #
# #         self.client.post('/class_car/', data={
# #             "id": 1,
# #             "name": "economy",
# #             "price": 1,
# #             "booking_time": 15
# #         })
# #         self.client.post('/cars/', data=Trip_get_test_me.payload_car)
# #
# #         Profile.objects.all().update(is_admin=False)
# #
# #     def api_authentication(self):
# #         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
# #
# #     def test_users(self):
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/me/trips')
# #         self.assertEqual(response.status_code, 200)
# #
# #     def test_users_not_admin(self):
# #         self.api_authentication()
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/me/trips')
# #         self.assertEqual(response.status_code, 200)
# #
# #
# #
# # class Trip_get_not_current_test_pk(APITestCase):
# #
# #     def setUp(self):
# #         self.user = self.client.post('/users/signup',
# #                                      data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
# #                                            "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
# #
# #         response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
# #         self.token = response.data['access']
# #         payload = {
# #             "price_for_km": 23,
# #             "night_add": 13,
# #             "price_dtp": 8,
# #             "parking_price": 9,
# #             "booking_price": 23,
# #             "description": "very informative"
# #         }
# #
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #         self.client.post('/price/', data=payload)
# #
# #         self.client.post('/class_car/', data={
# #             "id": 1,
# #             "name": "economy",
# #             "price": 1,
# #             "booking_time": 15
# #         })
# #         self.client.post('/cars/', data=Trip_get_test_me.payload_car)
# #
# #         Profile.objects.all().update(is_admin=False)
# #         self.user_id = Profile.objects.all()[0].id
# #     def api_authentication(self):
# #         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
# #
# #     def test_users(self):
# #         self.api_authentication()
# #         Profile.objects.all().update(is_admin=True)
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/{}/trips'.format(self.user_id))
# #         self.assertEqual(response.status_code, 200)
# #
# #     def test_users_not_admin_his_pk(self):
# #         self.api_authentication()
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/{}/trips'.format(self.user_id))
# #         self.assertEqual(response.status_code, 200)
# #
# #     def test_users_not_admin_and_not_his_pk(self):
# #         self.api_authentication()
# #
# #         self.client.get('/cars/free/?latitude=55&longitude=37&distance=100&class_car=economy&ordering=distance')
# #
# #         id_car = ViewedCars.objects.all()[0].id
# #         self.client.post('/cars/{}/book'.format(id_car))
# #         self.client.post('/trip/start/{}'.format(id_car))
# #
# #         response = self.client.get('/users/{}/trips'.format(self.user_id+1))
# #         self.assertEqual(response.status_code, 401)
