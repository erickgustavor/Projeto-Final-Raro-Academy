from django import forms
from account.models import Account

class TransactionForm(forms.Form):
    to_account = forms.CharField(
        label="Conta de Destino",
        max_length=11,
        widget=forms.TextInput(attrs={'placeholder': 'Digite CPF da conta destino'}),
        required=True
    )

    amount = forms.DecimalField(
        label="Valor da Transferência",
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Insira o valor da transferência'})
    )

    def clean(self):
        cleaned_data = super().clean()
        if not Account.objects.filter(cpf = cleaned_data.get('to_account')).exists():
            self.add_error('to_account', 'Conta de destino não encontrada')
        return cleaned_data


