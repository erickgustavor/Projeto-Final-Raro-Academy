from django import forms
from account.models import Account


class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=150, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = Account
        fields = ["email", "password"]

    def clean(self):
        return self.data
