from django import forms
from django.contrib.auth import authenticate
from account.models import Account

class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=150, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = Account
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError("Email ou senha inválidos.")

        return cleaned_data
