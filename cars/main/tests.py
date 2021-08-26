from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .test_factories import UserFactory,ProfileFactory
from .models import Profile
from rest_framework_jwt import utils, views
from rest_framework.test import APIClient


# from rest_framework_jwt.settings import api_settings
#
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

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
    # factory
    def get_token(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/auth-token/', self.data, format='json')
        return response.data['token']

    def create_token(self, user, exp=None, orig_iat=None):
        payload = utils.jwt_payload_handler(user)
        if exp:
            payload['exp'] = exp

        if orig_iat:
            payload['orig_iat'] = timegm(orig_iat.utctimetuple())

        token = utils.jwt_encode_handler(payload)
        return token


    def setUp(self):
        # profile = ProfileFactory()
        # payload = jwt_payload_handler(profile.user)
        # self.token = self.create_token(profile.user)
        # raise Exception(self.token)
        # p = Profile.objects.all()
        self.client.post(reverse('signup'),
                         data={'username': 'test1234', 'password': 'test123123', 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': '2003-09-09'})
        # raise Exception(p,Profile.objects.all())

        # raise Exception(Profile.objects.all()[0].is_admin)
        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        # response = self.client.post(reverse('signin'), data={'username':profile.user.username , 'password': profile.user.password})
        # raise Exception(response)
        self.token = response.data['access']
        # self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        Profile.objects.all().update(is_admin=True)

        # self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
        # response = self.client.get(reverse('health'))

        self.api_authentication()
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
        self.client.post(reverse('signup'),
                         data={'username': 'test123', 'password': 'test123123', 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': '2003-09-09'})

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
class UserGetTestPk(APITestCase):

    def setUp(self):
        self.client.post(reverse('signup'),
                         data={'username': 'test123', 'password': 'test123123', 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': '2003-09-09'})
        # raise Exception(self.user)
        # raise Exception(Profile.objects.all()[0].is_admin)
        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id
        # self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/{}'.format(self.user_id))
        # response = self.client.get('users_me'.format(self.user_id))

        # response = self.client.get(reverse('users',args = {'pk':self.user_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_his_pk(self):
        self.api_authentication()
        # Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/{}'.format(self.user_id))
        # raise Exception(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_and_not_his_pk(self):
        self.api_authentication()
        response = self.client.get('/users/{}'.format(self.user_id + 1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_not_auth(self):
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#

class UserPatchTestMe(APITestCase):

    def setUp(self):
        self.client.post(reverse('signup'),
                         data={'username': 'test123', 'password': 'test123123', 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': '2003-09-09'})
        # raise Exception(self.user)
        # raise Exception(Profile.objects.all()[0].is_admin)
        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        # raise Exception(response)
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id
        # self.api_authentication()

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
        self.client.post(reverse('signup'),
                         data={'username': 'test123', 'password': 'test123123', 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': '2003-09-09'})

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
        response = self.client.get('/users/{}'.format(self.user_id + 1), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_not_auth(self):
        response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDeleteTestMe(APITestCase):

    def setUp(self):
        self.client.post(reverse('signup'),
                         data={'username': 'test123', 'password': 'test123123', 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': '2003-09-09'})

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
        # self.user =
        self.client.post(reverse('signup'),
                         data={'username': 'test123', 'password': 'test123123', 'dtp_times': 9,
                               'email': 'test@gmail.com', 'date_of_birth': '2003-09-09'})

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
        response = self.client.get('/users/{}'.format(self.user_id + 1))
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_not_auth(self):
        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
