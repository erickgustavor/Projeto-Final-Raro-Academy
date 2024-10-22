from django import forms
from .models import Account

class AccountRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Senha'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmar Senha'
    )

    class Meta:
        model = Account
        fields = ['username', 'email', 'cpf', 'password', 'confirm_password']
        labels = {
            'username': 'Nome',
            'email': 'E-mail',
            'cpf': 'CPF',
        }
        error_messages = {
            'username': {
                'required': 'Este campo é obrigatório.',
            }
        }

