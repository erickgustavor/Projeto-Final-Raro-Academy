from django import forms
from account.models import Account
from account.validations.registration_validations import (
    validate_cpf,
    validate_username,
    validate_email,
    validate_password,
)


class AccountRegistrationForm(forms.ModelForm):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar Senha"
    )

    class Meta:
        model = Account
        fields = ["username", "email", "cpf", "password", "confirm_password"]
        labels = {
            "username": "Nome",
            "email": "E-mail",
            "cpf": "CPF",
        }
        error_messages = {
            "username": {
                "required": 'O campo "Nome" é obrigatório.',
            }
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        validate_cpf(cpf)
        return cpf

    def clean_username(self):
        username = self.cleaned_data.get("username")
        validate_username(username)
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_email(email)
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        validate_password(password, confirm_password)

        return cleaned_data

