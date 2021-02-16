from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from faker import Faker


class AccountTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        faker = Faker()
        cls._test_email = faker.safe_email()
        cls._test_password = 'secret'
        cls._test_fname = faker.first_name()
        cls._test_lname = faker.last_name()

    def test_create_and_login_account(self):
        """
        Ensure we can create user and login.
        """
        data = {
            'email': self._test_email,
            'password': self._test_password,
            'first_name': self._test_fname,
            'last_name': self._test_lname
        }

        # Create user
        response = self.client.post(
            reverse('create-user'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email=self._test_email).count(), 1)

        # Login user
        response = self.client.post(
            reverse('login'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
