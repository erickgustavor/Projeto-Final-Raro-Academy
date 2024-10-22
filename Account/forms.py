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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data

