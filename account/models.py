from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from enum import Enum
from django.contrib.auth.hashers import make_password, check_password


class AccountType(Enum):
    FREE = "free"
    PREMIUM = "premium"
    ADMIN = "admin"

    @classmethod
    def choices(cls):
        return [(item.value, item.name.capitalize()) for item in cls]


class AccountManager(BaseUserManager):
    def create_user(self, username, email, cpf, password, save=False, **extra_fields):
        if not username:
            raise ValueError("O nome de usuário é obrigatório")
        if not email:
            raise ValueError("O email é obrigatório")
        if not cpf:
            raise ValueError("O CPF é obrigatório")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, cpf=cpf, **extra_fields)
        user.set_password(password)
        if save:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, cpf, password, **extra_fields)


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
