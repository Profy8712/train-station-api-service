from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = None  # Remove username field completely

    USERNAME_FIELD = "email"  # Use email as the login field
    REQUIRED_FIELDS = []  # Remove username from required fields

    def __str__(self):
        return self.email

    @classmethod
    def create_superuser(cls, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return cls._create_user(email=email, password=password, **extra_fields)
    

