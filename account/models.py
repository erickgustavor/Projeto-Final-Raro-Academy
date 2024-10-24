from enum import Enum

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import AccountManager


class AccountType(Enum):
    FREE = "free"
    PREMIUM = "premium"
    ADMIN = "admin"

    @classmethod
    def choices(cls):
        return [(item.value, item.name.capitalize()) for item in cls]


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    type = models.CharField(
        max_length=10, choices=AccountType.choices(), default=AccountType.FREE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["cpf", "username"]

    objects = AccountManager()

    def __str__(self):
        return self.email
