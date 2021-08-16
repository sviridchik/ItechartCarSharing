from rest_framework.test import APITestCase
from .models import *
from django.test import Client
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



#++++++++++++++++++++++ price +++++++++++++++++++++++++++++++++++++++++++++++
class Price_post_test(APITestCase):


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



    def test_price(self):
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
        response = self.client.post('/price/',data=payload)
        # raise Exception(Price.objects.all()[0].description)
        self.assertEqual(response.status_code, 201)

    def test_price_not_admin(self):
        self.api_authentication()
        # Profile.objects.all().update(is_admin=True)
        response = self.client.post('/price',
                                    data={
                                        "price_for_km": 23,
                                        "night_add": 13,
                                        "price_dtp": 8,
                                        "parking_price": 9,
                                        "booking_price": 23,
                                        "description": "very informative"
                                    })
        self.assertEqual(response.status_code, 401)

    def test_price_not_auth(self):
        # self.api_authentication()
        # Profile.objects.all().update(is_admin=True)
        response = self.client.post('/price',
                                    data={
                                        "price_for_km": 23,
                                        "night_add": 13,
                                        "price_dtp": 8,
                                        "parking_price": 9,
                                        "booking_price": 23,
                                        "description": "very informative"
                                    })
        self.assertEqual(response.status_code, 401)

#
class Price_get_test(APITestCase):

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



    def test_price(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        response = self.client.get('/price/')
        # raise Exception(response.data)
        self.assertEqual(response.status_code, 200)

    def test_price_not_admin(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        Profile.objects.all().update(is_admin=False)
        # raise Exception(Price.objects.all())

        response = self.client.get('/price/')
        self.assertEqual(response.status_code, 200)

    def test_price_not_auth(self):
        # self.api_authentication()
        # Profile.objects.all().update(is_admin=True)
        response = self.client.get('/price/')
        self.assertEqual(response.status_code, 401)


#
class Price_get_test_pk(APITestCase):

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

    def test_price(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        id = Price.objects.all()[0].id
        response = self.client.get('/price/{}'.format(id))
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        Profile.objects.all().update(is_admin=False)
        id = Price.objects.all()[0].id
        response = self.client.get('/price/{}'.format(id))
        self.assertEqual(response.status_code, 200)


    def test_users_not_auth(self):
        response = self.client.get('/price/{}'.format(1))
        self.assertEqual(response.status_code, 401)



class Price_patch_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_price(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        id = Price.objects.all()[0].id
        response = self.client.patch('/price/{}'.format(id),data = {"price_dtp": 3,})
        self.assertEqual(Price.objects.get(pk=id).price_dtp, 3)
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        Profile.objects.all().update(is_admin=False)
        id = Price.objects.all()[0].id
        response = self.client.patch('/price/{}'.format(id), data={"price_dtp": 3, })
        self.assertEqual(Price.objects.get(pk=id).price_dtp, 8)
        self.assertEqual(response.status_code, 401)


    # def test_users_not_auth(self):
    #     response = self.client.patch('/price/{}'.format(id), data={ })
    #     self.assertEqual(response.status_code, 401)



class Price_delete_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_price(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        id = Price.objects.all()[0].id
        response = self.client.delete('/price/{}'.format(id))
        self.assertEqual(response.status_code, 204)

    def test_users_not_admin(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        Profile.objects.all().update(is_admin=False)
        id = Price.objects.all()[0].id
        response = self.client.delete('/price/{}'.format(id))
        self.assertEqual(response.status_code, 401)


    def test_users_not_auth(self):
        response = self.client.delete('/price/{}'.format(1))
        self.assertEqual(response.status_code, 401)

# +++++++++++++++++++++++++++++++++++++++++ class ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Class_post_test(APITestCase):


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



    def test_class(self):
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
        response = self.client.post('/price/',data=payload)

        response = self.client.post('/class/',data= {
        "id": 1,
        "name": "comfort",
        "price": 1,
        "booking_time": 15
    })
        # raise Exception(Price.objects.all()[0].description)
        self.assertEqual(response.status_code, 201)

    def test_price_not_admin(self):
        self.api_authentication()
        # Profile.objects.all().update(is_admin=True)
        response = self.client.post('/price',
                                    data={
                                        "price_for_km": 23,
                                        "night_add": 13,
                                        "price_dtp": 8,
                                        "parking_price": 9,
                                        "booking_price": 23,
                                        "description": "very informative"
                                    })
        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        self.assertEqual(response.status_code, 401)
    #
    def test_price_not_auth(self):
        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        self.assertEqual(response.status_code, 401)


class Price_get_test(APITestCase):

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

    def test_price(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        response = self.client.get('/class/')
        # raise Exception(response.data)
        self.assertEqual(response.status_code, 200)

    def test_price_not_admin(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        Profile.objects.all().update(is_admin=False)
        # raise Exception(Price.objects.all())

        response = self.client.get('/class/')
        self.assertEqual(response.status_code, 200)

    def test_price_not_auth(self):
        # self.api_authentication()
        # Profile.objects.all().update(is_admin=True)
        response = self.client.get('/class/')
        self.assertEqual(response.status_code, 401)


class Price_get_test_pk(APITestCase):

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

    def test_price(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        id = Class_car.objects.all()[0].id
        response = self.client.get('/class/{}'.format(id))
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })

        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        Profile.objects.all().update(is_admin=False)

        # raise Exception(Class_car.objects.all())
        id = Class_car.objects.all()[0].id
        response = self.client.get('/class/{}'.format(id))
        self.assertEqual(response.status_code, 200)


    def test_users_not_auth(self):
        response = self.client.get('/class/{}'.format(1))
        self.assertEqual(response.status_code, 401)


class Class_patch_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_price(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        id = Class_car.objects.all()[0].id
        response = self.client.patch('/class/{}'.format(id),data = {"booking_time": 21,})
        self.assertEqual(Class_car.objects.get(pk=id).booking_time, 21)
        self.assertEqual(response.status_code, 200)

    def test_users_not_admin(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        Profile.objects.all().update(is_admin=False)
        id = Class_car.objects.all()[0].id
        response = self.client.patch('/class/{}'.format(id),data = {"booking_time": 21,})
        self.assertEqual(Class_car.objects.get(pk=id).booking_time, 15)
        self.assertEqual(response.status_code, 401)


    # def test_users_not_auth(self):
    #     response = self.client.patch('/class/{}'.format(id), data={"booking_time": 21, })
    #     self.assertEqual(response.status_code, 401)



class Class_delete_test_pk(APITestCase):

    def setUp(self):
        self.user = self.client.post('/users/signup',
                                     data={'username': 'test123', 'password': 'test123123', "dtp_times": 9,
                                           "email": "test@gmail.com", "date_of_birth": "2003-09-09"})

        response = self.client.post('/users/signin', data={'username': 'test123', 'password': 'test123123'})
        self.token = response.data['access']
        self.user_id = Profile.objects.all()[0].id

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_price(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        id = Class_car.objects.all()[0].id
        response = self.client.delete('/class/{}'.format(id))
        # raise Exception(Class_car.objects.all())

        self.assertEqual(response.status_code, 204)

    def test_users_not_admin(self):
        self.api_authentication()
        Profile.objects.all().update(is_admin=True)
        self.client.post('/price',
                         data={
                             "price_for_km": 23,
                             "night_add": 13,
                             "price_dtp": 8,
                             "parking_price": 9,
                             "booking_price": 23,
                             "description": "very informative"
                         })
        response = self.client.post('/class/', data={
            "id": 1,
            "name": "comfort",
            "price": 1,
            "booking_time": 15
        })
        Profile.objects.all().update(is_admin=False)
        id = Class_car.objects.all()[0].id
        response = self.client.delete('/class/{}'.format(id))
        self.assertEqual(response.status_code, 401)
#
#
#     def test_users_not_auth(self):
#         response = self.client.delete('/class/{}'.format(1))
#         self.assertEqual(response.status_code, 401)
