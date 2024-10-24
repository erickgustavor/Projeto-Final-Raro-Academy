from django.db import models
from django.utils import timezone
from Account.models import Account


class ProductInvestment(models.Model):
    name = models.CharField(max_length=100)
    tax = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Taxa anual do produto"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    minimum_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class Investment(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInvestment, on_delete=models.CASCADE)
    applied_value = models.DecimalField(max_digits=10, decimal_places=2)
    accumulated_income = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    investment_data = models.DateTimeField(default=timezone.now)
    rescue_data = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("ativo", "Ativo"),
            ("resgatado", "Resgatado"),
            ("vencido", "Vencido"),
        ],
        default="ativo",
    )

    def __str__(self):
        return f"Investimento de {self.Account} no produto {self.product.name}"
