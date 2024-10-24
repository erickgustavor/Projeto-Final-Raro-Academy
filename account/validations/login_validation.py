from django.contrib.auth.hashers import check_password

from account.models import Account


def validate_login(email, password):
    try:
        # Busca o usuário pelo email
        user = Account.objects.get(email=email)

        # Usa a função check_password do Django para verificar a senha
        if user.check_password(password):
            return user, None
        else:
            return None, "Senha inválida."
    except Account.DoesNotExist:
        return None, "Usuário não encontrado."
