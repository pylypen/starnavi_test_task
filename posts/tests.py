from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from posts.models import Post
from users.models import User
from faker import Faker


class AccountTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase
        """
        faker = Faker()
        cls._post_title = faker.text(max_nb_chars=120)
        cls._post_description = faker.text(max_nb_chars=1000)

        # Create User
        cls._test_user = User()
        cls._test_user.email = faker.safe_email()
        cls._test_user.first_name = faker.first_name()
        cls._test_user.last_name = faker.last_name()
        cls._test_user.password = make_password('secret')
        cls._test_user.save()

        # Create Post
        cls._test_post = Post()
        cls._test_post.title = faker.text(max_nb_chars=120)
        cls._test_post.description = faker.text(max_nb_chars=1000)
        cls._test_post.user = cls._test_user
        cls._test_post.save()

        # Create JWT token for user
        cls._refresh_token = RefreshToken.for_user(cls._test_user).access_token

    def test_create_post(self):
        """
        Ensure we can create post.
        """
        data = {
            'title': self._post_title,
            'description': self._post_description
        }

        # Create post
        token = f'Bearer {self._refresh_token}'
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(
            reverse('post-create'),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_post(self):
        """
        Ensure we can like and unlike post.
        """
        token = f'Bearer {self._refresh_token}'
        self.client.credentials(HTTP_AUTHORIZATION=token)

        # Like post
        response = self.client.post(
            reverse('post-like', kwargs={'pk': self._test_post.id}),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Unlike post
        response = self.client.delete(
            reverse('post-like', kwargs={'pk': self._test_post.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
