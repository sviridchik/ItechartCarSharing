from rest_framework.test import APITestCase
from .models import *

req_test_health = {}


class NoRightstest(APITestCase):

    # 401 Unauthorized Error
    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 401)


class My_Authtest(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)


class Logouttest2(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})
        response = self.client.post('/auth/jwt/create/', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        response = self.client.post('users/logout', HTTP_AUTHORIZATION='Bearer ' + self.token)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # 401 Unauthorized Error
    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 401)


class User_get_test(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        # raise Exception(Profile.objects.all()[0].is_admin)
        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        # self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
        # Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 401)

    def test_users_not_auth(self):
        # self.api_authentication()
        # Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 401)


class User_get_test_me(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, 200)

    def test_users_not_auth(self):
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, 401)


class User_get_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        # raise Exception(Profile.objects.all()[0].is_admin)
        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id
        # self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/{}'.format(self.user_id))
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin_his_pk(self):
        self.api_authentication()
        # Profile.objects.all().update(is_admin=True)
        response = self.client.get('/users/{}'.format(self.user_id))
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin_and_not_his_pk(self):
        self.api_authentication()
        response = self.client.get('/users/{}'.format(self.user_id + 1))
        self.assertEqual(response.status_code, 401)

    def test_users_not_auth(self):
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, 401)


class User_patch_test_me(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.patch('/users/me', data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
        response = self.client.patch('/users/me', data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, 200)

    #
    def test_users_not_auth(self):
        response = self.client.patch('/users/me', data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, 401)

    def test_users_invalid_field(self):
        self.api_authentication()
        response = self.client.patch('/users/me', data={"parents": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, 400)


class User_patch_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin_his_pk(self):
        self.api_authentication()
        response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin_and_not_his_pk(self):
        self.api_authentication()
        response = self.client.get('/users/{}'.format(self.user_id + 1), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, 401)

    def test_users_not_auth(self):
        response = self.client.get('/users/{}'.format(self.user_id), data={"email": "abracadabra@gmail.com"})
        self.assertEqual(response.status_code, 401)


class User_delete_test_me(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.delete('/users/me')

        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
        response = self.client.delete('/users/me')
        self.assertEqual(len(Profile.objects.all()), 0)

        self.assertEqual(response.status_code, 200)

    # #
    def test_users_not_auth(self):
        response = self.client.delete('/users/me')
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, 401)


class User_delete_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)

        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin_his_pk(self):
        self.api_authentication()
        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 0)
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin_and_not_his_pk(self):
        self.api_authentication()
        response = self.client.get('/users/{}'.format(self.user_id + 1))
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, 401)

    def test_users_not_auth(self):
        response = self.client.delete('/users/{}'.format(self.user_id))
        self.assertEqual(len(Profile.objects.all()), 1)
        self.assertEqual(response.status_code, 401)
