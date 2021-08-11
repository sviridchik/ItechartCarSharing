from rest_framework.test import APITestCase

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
