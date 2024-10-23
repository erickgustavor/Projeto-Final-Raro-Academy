from django.core.exceptions import ValidationError
import re
from .models import Account

def validate_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 digítos.')

    if cpf in ("00000000000", "11111111111", "22222222222", 
               "33333333333", "44444444444", "55555555555", 
               "66666666666", "77777777777", "88888888888", 
               "99999999999"):
        raise ValidationError('CPF Invalido.')

    if Account.objects.filter(cpf=cpf).exists():
        raise ValidationError('Já existe uma conta com este CPF.')


def validate_username(username):

    if not re.match(r'^[A-Za-záàãâéêíóôúç\'\- ]+$', username):
        raise ValidationError('O nome só pode conter letras, espaços, apóstrofos e hífens.')
    
    formatted_username = ' '.join(word.capitalize() for word in username.split())
    return formatted_username


def validate_email(email):

    if Account.objects.filter(email=email).exists():
        raise ValidationError('Já existe uma conta com este E-mail.')
    
    
def validate_password(password, confirm_password):
    if password != confirm_password:
        raise ValidationError('As senhas não coincidem.')
