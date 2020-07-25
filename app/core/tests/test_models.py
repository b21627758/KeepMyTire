from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@test.com', password='!TesT123.!'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_ok(self):
        """Test creating new user with email instead of username"""
        email = 'test@test.com'
        password = 'TEst123456.!'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_with_normalized_email(self):
        """Test new user email normalized"""
        email = 'test@TEST.com'
        user = get_user_model().objects.create_user(email, 'TEst123.!')

        self.assertEqual(user.email, email.lower())

    def test_creating_with_empty_email(self):
        """Test creating a user without email error, base create user test"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'TEst123.!')

    def test_create_superuser(self):
        """Test creating a superuser/owner"""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'Test123.!'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    """def test_create_from_customer(self):
        "Test create a user from already exists record (activate account)"
        get_user_model().objects.create_user(email='test@test.com')
        user = get_user_model().objects.create_user('test@test.com', 'Test123.!')

        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('Test123.!'))"""

    def test_create_without_password_user(self):
        """Test create without password (User FAIL)"""
        with self.assertRaises(ValueError):
            get_user_model().objects.register(email='test@test.com', password=None)

    def test_create_without_password_superuser(self):
        """Test create without password (creating
        nonactive user/customer)"""
        email = 'testcustomer@test.com'
        user = get_user_model().objects.create_customer(email=email)

        self.assertEqual(user.email, email)
        self.assertFalse(user.is_active)
        self.assertFalse(user.has_usable_password())
