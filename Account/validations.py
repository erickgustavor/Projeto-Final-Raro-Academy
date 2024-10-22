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