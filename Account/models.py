from django.db import models
from enum import Enum
from django.contrib.auth.hashers import make_password

class AccountType(Enum):
    FREE = "free"
    PREMIUM = "premium"
    ADMIN = "admin"

    @classmethod
    def choices(cls):
        return [(item.value, item.name.capitalize()) for item in cls]


class Account(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    cpf = models.CharField(max_length=11)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    type = models.CharField(
        max_length = 10, 
        choices = AccountType.choices(),
        default = AccountType.FREE.value
    )

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.type})"


