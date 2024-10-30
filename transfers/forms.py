from django import forms
from django.core.exceptions import ValidationError
from .models import Account, Transaction


class TransactionForm(forms.Form):
    to_account = forms.ModelChoiceField(
        label="Conta de Destino",
        queryset=Account.objects.none(),
        required=True,
        empty_label="Selecione a conta de destino",
        to_field_name="cpf",
    )

    amount = forms.DecimalField(
        label="Valor da Transferência",
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(
            attrs={"placeholder": "Insira o valor da transferência"}
        ),
    )

    def __init__(self, *args, user=None, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            to_accounts_cpf = Transaction.objects.filter(from_account=user).values_list(
                "to_account", flat=True
            )
            to_accounts = Account.objects.filter(cpf__in=to_accounts_cpf)
            self.fields["to_account"].queryset = to_accounts

    def clean(self):
        cleaned_data = super().clean()
        to_account = cleaned_data.get("to_account")
        if not to_account:
            raise ValidationError("Conta de destino não encontrada")
        return cleaned_data
