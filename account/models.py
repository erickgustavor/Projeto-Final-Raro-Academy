from enum import Enum
from uuid import uuid4
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
    username = models.CharField(max_length=100, verbose_name="nome de usuário")
    email = models.EmailField(max_length=100, unique=True)
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="saldo"
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    type = models.CharField(
        max_length=10,
        choices=AccountType.choices(),
        default=AccountType.FREE,
        verbose_name="tipo de conta",
    )

    contacts = models.ManyToManyField('Account', related_name='contact_accounts')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["cpf", "username"]

    objects = AccountManager()

    def __str__(self):
        return self.email


class RecoveryToken(models.Model):
    value = models.CharField(default=uuid4, max_length=200)
    is_active = models.BooleanField(default=True)
    account = models.ForeignKey(Account, related_name="token", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
