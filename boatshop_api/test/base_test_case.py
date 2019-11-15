from django.core.management import call_command
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    USER_ID_1 = 1
    USER_ID_2 = 2
    USER_ID_3 = 3
    USER_ID_4_NOT_EXIST = 4

    BOAT_ID_1 = 1
    BOAT_ID_2 = 2
    BOAT_ID_3 = 3
    BOAT_ID_4_NOT_EXIST = 4

    ORDER_ID_1 = 1
    ORDER_ID_2 = 2
    ORDER_ID_3 = 3
    ORDER_ID_4 = 4
    ORDER_ID_5_NOT_EXIST = 5

    USER_DEFAULT_PASSWORD = "adminadmin"

    ORDER_KEYS = set(['boat', 'buyer', 'approved', 'id'])
    BOAT_KEYS = set(['owner', 'boat', 'price', 'id'])

    def setUp(self):
        call_command('loaddata', 'fixtures.json', verbosity=0)

    def before_test(self, user_id):
        self.user = User.objects.filter(pk=user_id).first()
        if self.user:
            resp = self.client.post(reverse('get-token'),
                                    {'username': self.user.username, 'password': self.USER_DEFAULT_PASSWORD},
                                    format='json')
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertTrue('token' in resp.data)
            self.token = resp.data.get('token')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        else:
            self.token = None
            self.client.credentials(HTTP_AUTHORIZATION='JWT')
        return self.user
