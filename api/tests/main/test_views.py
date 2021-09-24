from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse
# from .models import Profile
from rest_framework import status
from rest_framework.test import APITestCase
import uuid

# from .test_factories import ProfileFactory

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
