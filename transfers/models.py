from django.db import models
from account.models import Account

# Create your models here.

class Transaction(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field='cpf', related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field='cpf', related_name='to_account')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transferência de {self.from_account} para {self.to_account} no valor de R${self.amount} em {self.timestamp}"
