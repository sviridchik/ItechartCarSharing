import uuid
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Profile
# from users.models import Profile

from .factories import ProfileFactory


class MyAuthTest(APITestCase):

    def setUp(self):
        self.login = 'test123'
        self.password = 'test123123'
        self.client.post(reverse('signup'),
                         data={'username': self.login, 'password': self.password, 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': "2000-09-09"})
        response = self.client.post(reverse('signin'), data={'username': self.login, 'password': self.password})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_health(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutTest2(APITestCase):

    def setUp(self):
        self.login = 'test123'
        self.password = 'test123123'
        self.client.post(reverse('signup'), data={'username': self.login, 'password': self.password, 'dtp_times': 9,
                                                  'email': 'test@gmail.com', 'date_of_birth': '2003-09-09'})
        response = self.client.post('/auth/jwt/create/', data={'username': self.login, 'password': self.password})
        self.token = response.data['access']
        self.client.post(reverse('logout'), HTTP_AUTHORIZATION='Bearer ' + self.token)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_health(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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


class UserGetTest(PseudoAuth):

    def test_users(self):
        Profile.objects.all().update(is_admin=True)
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NotAuthTest(APITestCase):
    def setUp(self):
        ProfileFactory()

    def test_users_not_auth_get(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_not_auth_get_me(self):
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_not_auth_patch(self):
        response = self.client.patch('/users/me', data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_not_auth_patch_pk(self):
        self.user_id = Profile.objects.all()[0].id

        response = self.client.patch('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_not_auth_delete(self):
        response = self.client.delete('/users/me')
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_not_auth_delete_pk(self):
        self.user_id = Profile.objects.all()[0].id

        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserGetTestMe(PseudoAuth):

    def test_users(self):
        Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin(self):
        Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserGetTestPk(PseudoAuth):

    def test_users(self):
        self.user_id = Profile.objects.all()[0].id
        Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/{}'.format(self.user_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_his_pk(self):
        self.user_id = Profile.objects.all()[0].id

        response = self.client.get('/users/{}'.format(self.user_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserGetTestPkNotGood(PseudoAuth):

    def test_users_not_admin_his_pk(self):
        self.user_id = Profile.objects.all()[0].id

        response = self.client.get('/users/{}'.format(self.user_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_and_not_his_pk(self):
        not_his_pk = uuid.uuid4()
        response = self.client.get('/users/{}'.format(not_his_pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserPatchTestMe(PseudoAuth):

    def test_users(self):
        Profile.objects.all().update(is_admin=True)
        response = self.client.patch('/users/me', data={"email": "abracadabra12@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_kosak(self):
        Profile.objects.all().update(is_admin=True)
        response = self.client.patch('/users/me', data={"dtp_times": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin(self):
        response = self.client.patch('/users/me', data={"email": "abracadabra123@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserPatchTestPk(PseudoAuth):

    def test_users(self):
        Profile.objects.all().update(is_admin=True)
        self.user_id = Profile.objects.all()[0].id
        response = self.client.patch('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_his_pk(self):
        self.user_id = Profile.objects.all()[0].id

        response = self.client.patch('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_and_not_his_pk(self):
        not_his_pk = uuid.uuid4()
        response = self.client.patch('/users/{}'.format(not_his_pk), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteTestMe(PseudoAuth):

    def test_users(self):
        Profile.objects.all().update(is_admin=True)
        response = self.client.delete('/users/me')
        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_not_admin(self):
        response = self.client.delete('/users/me')
        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserDeleteTestPk(PseudoAuth):

    def test_users(self):
        Profile.objects.all().update(is_admin=True)
        self.user_id = Profile.objects.all()[0].id

        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_not_admin_his_pk(self):
        self.user_id = Profile.objects.all()[0].id
        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_not_admin_and_not_his_pk(self):
        not_his_pk = uuid.uuid4()
        response = self.client.get('/users/{}'.format(not_his_pk))
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
