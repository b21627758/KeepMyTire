from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:register')
CREATE_CUSTOMER_URL = reverse('user:create-customer')
CREATE_STAFF_URL = reverse('user:create-staff')


def create_user(**params):
    """Creating user while registration"""
    return get_user_model().objects.register(**params)


def create_customer(**params):
    """Creating customer"""
    return get_user_model().objects.create_customer(**params)


def create_new_staff(**params):
    """Creating new staff"""
    return get_user_model().objects.create_superuser(**params)


class PublicApiTest(TestCase):
    """Test the uses API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload successful"""
        payload = {
            'email': 'test@test.com',
            'password': 'Test123456',
            'first_name': 'Test',
            'last_name': 'Testoglu',
            'date_of_birth': '2019-12-21',
            'phone_number': '+905093456789'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'email': 'test@test.com',
            'password': 'Test123456',
            'first_name': 'Test',
            'last_name': 'Testoglu',
            'date_of_birth': '2019-12-21',
            'phone_num': '+905093456789'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        """Test password under required length"""
        payload = {
            'email': 'test@test.com',
            'password': 'Test',
            'first_name': 'Test',
            'last_name': 'Testoglu',
            'date_of_birth': '2019-12-21',
            'phone_num': '+905093456789'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_customer(self):
        """Test creating customer"""
        payload = {
            'email': 'test@test.com',
            'first_name': 'Test',
            'last_name': 'Testoglu',
            'date_of_birth': '2019-12-21',
            'phone_num': '+905093456789'
        }
        res = self.client.post(CREATE_CUSTOMER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertEqual(user.email, payload['email'])
        self.assertFalse(user.has_usable_password())
        self.assertFalse(user.is_active)
        self.assertNotIn('password', res.data)

    def test_create_user_from_customer(self):
        """Test create user from already existent customer record"""
        payload = {
            'email': 'test@test.com',
            'first_name': 'Test',
            'last_name': 'Testoglu',
            'date_of_birth': '2019-12-21',
            'phone_num': '+905093456789'
        }

        customer = create_customer(**payload)

        payload['password'] = 'TEst123445546'

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.is_active)
        self.assertEqual(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
