# from class_cars.models import *
# from class_cars.models import ClassCar
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User, Permission
# from price.models import Price
# from rest_framework import status
# from rest_framework.test import APITestCase
# from tests.class_cars.factories import ClassFactory
# from tests.price.factories import PriceFactory
# from tests.users.factories import ProfileFactory
# from users.models import Profile
#
#
# class PseudoAuth(APITestCase):
#     def setUp(self):
#         profile = ProfileFactory()
#         ps = profile.user.password
#         self.user = profile.user
#
#         self.client.force_authenticate(self.user)
#         User.objects.filter(username=profile.user.username).update(password=make_password(ps))
#         permission = Permission.objects.all()
#         for p in permission:
#             self.user.user_permissions.add(p)
#         ClassFactory()
#
#
# class ClassNotAuth(APITestCase):
#
#     def setUp(self):
#         ProfileFactory()
#         ClassFactory()
#         self.id = Price.objects.all()[0].id
#         self.id_class = ClassCar.objects.all()[0].id
#
#     def test_class_not_auth_post(self):
#         response = self.client.post('/class/', data={
#             "name": "comfort",
#             "price": self.id,
#             "booking_time": 15
#         })
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_class_not_auth_get(self):
#         response = self.client.get('/class/')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_class_not_auth(self):
#         response = self.client.get('/class/{}'.format(self.id_class))
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_class_not_admin_delete(self):
#         response = self.client.delete('/class/{}'.format(self.id_class))
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class ClassPostTest(APITestCase):
#     def setUp(self):
#         profile = ProfileFactory()
#         ps = profile.user.password
#         self.user = profile.user
#         self.client.force_authenticate(self.user)
#         User.objects.filter(username=profile.user.username).update(password=make_password(ps))
#         permission = Permission.objects.all()
#         for p in permission:
#             self.user.user_permissions.add(p)
#         PriceFactory()
#
#     def test_class(self):
#         Profile.objects.all().update(is_admin=True)
#         id = Price.objects.all()[0].id
#         response = self.client.post('/class/', data={
#             "name": "comfort",
#             "price": id,
#             "booking_time": 15
#         })
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(len(ClassCar.objects.all()), 1)
#
#     def test_class_not_admin(self):
#         id = Price.objects.all()[0].id
#
#         response = self.client.post('/class/', data={
#             "name": "comfort",
#             "price": id,
#             "booking_time": 15
#         })
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(ClassCar.objects.all()), 0)
#
#
# class ClassGetTest(PseudoAuth):
#
#     def test_class(self):
#         Profile.objects.all().update(is_admin=True)
#         response = self.client.get('/class/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_class_not_admin(self):
#         response = self.client.get('/class/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class ClassGetTestPk(PseudoAuth):
#
#     def test_class(self):
#         Profile.objects.all().update(is_admin=True)
#         id = ClassCar.objects.all()[0].id
#         response = self.client.get('/class/{}'.format(id))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_class_not_admin(self):
#         id = ClassCar.objects.all()[0].id
#         response = self.client.get('/class/{}'.format(id))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class ClassPatchTestPk(PseudoAuth):
#
#     def test_class(self):
#         Profile.objects.all().update(is_admin=True)
#         id = ClassCar.objects.all()[0].id
#         response = self.client.patch('/class/{}'.format(id), data={"booking_time": 21, })
#         self.assertEqual(ClassCar.objects.get(pk=id).booking_time, 21)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_class_not_admin(self):
#         id = ClassCar.objects.all()[0].id
#         response = self.client.patch('/class/{}'.format(id), data={"booking_time": 21, })
#         self.assertEqual(ClassCar.objects.get(pk=id).booking_time, 15)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#
# class ClassDeleteTestPk(PseudoAuth):
#
#     def test_class(self):
#         Profile.objects.all().update(is_admin=True)
#         id = ClassCar.objects.all()[0].id
#         response = self.client.delete('/class/{}'.format(id))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(len(ClassCar.objects.all()), 0)
