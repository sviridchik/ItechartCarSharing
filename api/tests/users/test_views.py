from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse
# from users.models import Profile
from users.views import ProfileList, ProfileDetailList
from rest_framework import status
from rest_framework.test import APITestCase
import uuid
from users.models import Profile
from .test_factories import ProfileFactory
from rest_framework_jwt.settings import api_settings
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

#
req_test_health = {}


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
        self.user = profile.user
        User.objects.filter(username=profile.user.username).update(password=make_password(ps))

        # response = self.client.post(reverse('signin'),
        #                             data={'username': profile.user.username, 'password': profile.user.password})
        # self.token = response.data['access']
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        #
        payload = jwt_payload_handler(profile.user)
        self.token = jwt_encode_handler(payload)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        factory = APIRequestFactory()
        view = ProfileList.as_view()
        # self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        # response = self.client.get(reverse('users'))
        request = factory.get(reverse('users'))
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin(self):
        factory = APIRequestFactory()
        view = ProfileList.as_view()
        # self.api_authentication()
        # response = self.client.get(reverse('users'))
        request = factory.get(reverse('users'))
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_not_auth(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserGetTestMe(APITestCase):

    def setUp(self):
        profile = ProfileFactory()
        self.user = profile.user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(profile.user)
        self.token = jwt_encode_handler(payload)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        Profile.objects.all().update(is_admin=True)
        factory = APIRequestFactory()
        view = ProfileList.as_view()
        Profile.objects.all().update(is_admin=True)
        request = factory.get('/users/me')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin(self):
        factory = APIRequestFactory()
        view = ProfileList.as_view()
        Profile.objects.all().update(is_admin=True)
        request = factory.get('/users/me')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_auth(self):
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


#

# #
class UserGetTestPk(APITestCase):

    def setUp(self):
        profile = ProfileFactory()
        self.user = profile.user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(profile.user)
        self.token = jwt_encode_handler(payload)
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        Profile.objects.all().update(is_admin=True)
        factory = APIRequestFactory()
        view = ProfileList.as_view()
        Profile.objects.all().update(is_admin=True)
        request = factory.get('/users/{}'.format(self.user_id))
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_his_pk(self):
        factory = APIRequestFactory()
        view = ProfileList.as_view()
        Profile.objects.all().update(is_admin=True)
        request = factory.get('/users/{}'.format(self.user_id))
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserGetTestPkNotGood(APITestCase):

    def setUp(self):
        profile = ProfileFactory()
        self.user = profile.user
        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users_not_admin_his_pk(self):
        self.api_authentication()
        response = self.client.get('/users/{}'.format(self.user_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_and_not_his_pk(self):
        self.api_authentication()
        not_his_pk = uuid.uuid4()
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

    def test_users_kosak(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.patch('/users/me', data={"dtp_times": 10})
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
        self.profile = ProfileFactory()
        response = self.client.post(reverse('signin'), data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        response = self.client.patch('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        # raise Exception(Profile.objects.all()[0].user.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_his_pk(self):
        self.api_authentication()
        response = self.client.patch('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_not_admin_and_not_his_pk(self):
        self.api_authentication()
        not_his_pk = uuid.uuid4()

        response = self.client.patch('/users/{}'.format(not_his_pk), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_not_auth(self):
        response = self.client.patch('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
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
