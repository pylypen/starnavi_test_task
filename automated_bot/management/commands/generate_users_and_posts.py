from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker
import random
import os
from users.models import User
from posts.models import Post, Like


class Command(BaseCommand):
    help = 'Generate seed'
    _number_users = 10
    _number_posts_per_user = 10
    _number_likes_per_post = 10
    _min_number_posts_per_user = 1
    _min_number_likes_per_post = 1
    _faker = Faker()

    def handle(self, *args, **options):
        if self._get_config() is False:
            self._print_error('Something is wrong with settings!')
            return None

        self._print_success('Creating users and posts')
        self._generate_users()
        print()
        self._print_success('Users and posts created')

        self._print_success('Creating likes')
        self._generate_post_likes()
        print()
        self._print_success('Likes created')

        self._print_success('Users, posts and likes successfully created!')

    def _generate_users(self):
        for i in range(self._number_users):
            user = User()
            user.email = str(i) + self._faker.safe_email()
            user.first_name = self._faker.first_name()
            user.last_name = self._faker.last_name()
            user.password = make_password('secret')
            user.save()

            self._generate_posts(user)

    def _generate_posts(self, user):
        print(f"Creating posts by {user.first_name} {user.last_name}", end="\r")
        for _ in range(random.randint(self._min_number_posts_per_user, self._number_posts_per_user)):
            post = Post()
            post.title = self._faker.text(max_nb_chars=120)
            post.description = self._faker.text(max_nb_chars=1000)
            post.user = user
            post.save()

    def _generate_post_likes(self):
        users = User.objects.all()[:10]
        for user in users:
            print(f"Creating likes by {user.first_name} {user.last_name}", end="\r")
            n_iteration = random.randint(self._min_number_likes_per_post, self._number_likes_per_post)
            for i in range(n_iteration):
                like = Like()
                like.user = user
                like.post = Post.objects.order_by('?').first()
                like.save()

    def _get_config(self):
        try:
            self._number_users = int(os.getenv('AUTOMATED_BOT_NUMBER_OF_USERS', self._number_users))
            self._number_posts_per_user = int(os.getenv('AUTOMATED_BOT_MAX_POSTS_PER_USER', self._number_posts_per_user))
            self._number_likes_per_post = int(os.getenv('AUTOMATED_BOT_MAX_LIKES_PER_USER', self._number_likes_per_post))
        except ValueError:
            return False

        if self._number_users <= 1 or self._number_posts_per_user <= 1 or self._number_likes_per_post <= 1:
            return False

        return True

    def _print_success(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def _print_error(self, message):
        self.stdout.write(self.style.ERROR(message))
