from django.core.exceptions import ValidationError
import re

def validate_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11:
        raise ValidationError('CPF must have 11 digits.')

    if cpf in ("00000000000", "11111111111", "22222222222", 
               "33333333333", "44444444444", "55555555555", 
               "66666666666", "77777777777", "88888888888", 
               "99999999999"):
        raise ValidationError('Invalid CPF.')

    from .models import Account
    if Account.objects.filter(cpf=cpf).exists():
        raise ValidationError('Account with this CPF already exists.')

def validate_username(username):
    from .models import Account
    if Account.objects.filter(username=username).exists():
        raise ValidationError('Account with this Username already exists.')

def validate_email(email):
    from .models import Account
    if Account.objects.filter(email=email).exists():
        raise ValidationError('Account with this Email already exists.')