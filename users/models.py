from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    User Model extends by AbstractUser
    """
    # unset username
    username = None

    email = models.EmailField(_('email address'), unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=128)
    last_name = models.CharField(_('last name'), max_length=150)
    location = models.CharField(_('location'), max_length=128, blank=True, null=True)
    bio = models.CharField(_('bio'), max_length=128, blank=True, null=True)
    site = models.CharField(_('site'), max_length=128, blank=True, null=True)
    avatar = models.CharField(_('avatar'), max_length=256, blank=True, null=True)

    # set username by email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.first_name
