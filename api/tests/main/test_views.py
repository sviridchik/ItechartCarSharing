from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import Profile
from rest_framework import status
from rest_framework.test import APITestCase
import uuid

from .test_factories import ProfileFactory

req_test_health = {}


class HealthTest(APITestCase):

    # 401 Unauthorized Error
    def test_health(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NoSlashTest(APITestCase):

    # 401 Unauthorized Error
    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)


class MyAuthTest(APITestCase):

    def setUp(self):
        self.client.post(reverse('signup'),
                         data={'username': 'test123', 'password': 'test123123', 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': "2003-09-09"})
        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_health(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutTest2(APITestCase):

    def setUp(self):
        self.client.post(reverse('signup'),
                         data={'username': 'test123', 'password': 'test123123', 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': '2003-09-09'})
        response = self.client.post('/auth/jwt/create/', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        response = self.client.post(reverse('logout'), HTTP_AUTHORIZATION='Bearer ' + self.token)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # 401 Unauthorized Error
    def test_health(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserGetTest(APITestCase):

    def setUp(self):
        profile = ProfileFactory()

        ps = profile.user.password
        User.objects.filter(username=profile.user.username).update(password=make_password(ps))

        response = self.client.post(reverse('signin'),
                                    data={'username': profile.user.username, 'password': profile.user.password})
        self.token = response.data['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin(self):
        self.api_authentication()
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_not_auth(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserGetTestMe(APITestCase):

    def setUp(self):
        profile = ProfileFactory()

        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin(self):
        self.api_authentication()

        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_auth(self):
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#
#
class UserGetTestPk(APITestCase):

    def setUp(self):
        profile = ProfileFactory()

        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id
        # raise Exception(self.user_id)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/{}'.format(self.user_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_his_pk(self):
        self.api_authentication()

        response = self.client.get('/users/{}'.format(self.user_id))
        # raise Exception(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_and_not_his_pk(self):
        self.api_authentication()
        # raise Exception(self.user_id[-1])
        not_his_pk = uuid.uuid4()
        # response = self.client.get('/users/{}'.format(str(int(self.user_id) + 1)))
        response = self.client.get('/users/{}'.format(not_his_pk))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    def test_users_not_auth(self):
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserPatchTestMe(APITestCase):

    def setUp(self):
        profile = ProfileFactory()

        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.patch('/users/me', data={"email": "abracadabra12@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin(self):
        self.api_authentication()
        response = self.client.patch('/users/me', data={"email": "abracadabra123@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #
    def test_users_not_auth(self):
        response = self.client.patch('/users/me', data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_invalid_field(self):
        self.api_authentication()
        response = self.client.patch('/users/me', data={"parents": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserPatchTestPk(APITestCase):

    def setUp(self):
        profile = ProfileFactory()

        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_his_pk(self):
        self.api_authentication()
        response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_and_not_his_pk(self):
        self.api_authentication()
        not_his_pk = uuid.uuid4()

        response = self.client.get('/users/{}'.format(not_his_pk), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_not_auth(self):
        response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDeleteTestMe(APITestCase):

    def setUp(self):
        profile = ProfileFactory()

        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.delete('/users/me')

        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_not_admin(self):
        self.api_authentication()
        response = self.client.delete('/users/me')
        self.assertEqual(len(Profile.objects.all()), 0)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # #
    def test_users_not_auth(self):
        response = self.client.delete('/users/me')
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDeleteTestPk(APITestCase):

    def setUp(self):
        profile = ProfileFactory()

        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_not_admin_his_pk(self):
        self.api_authentication()
        l = Profile.objects.all()
        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_not_admin_and_not_his_pk(self):
        self.api_authentication()
        not_his_pk = uuid.uuid4()

        response = self.client.get('/users/{}'.format(not_his_pk))
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_not_auth(self):
        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
