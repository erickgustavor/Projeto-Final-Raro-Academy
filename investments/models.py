from django.db import models
from django.utils import timezone
from account.models import Account
from .enums import IndexerEnum
from .utils import get_selic_rate, get_ipca_rate
from decimal import Decimal


class ProductInvestment(models.Model):
    INDEXER_CHOICES = [(
        indexer.value,
        indexer.name
        ) for indexer in IndexerEnum]

    name = models.CharField(max_length=100)
    tax = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Taxa anual do produto"
    )
    indexer_choice = models.CharField(
        max_length=5,
        choices=INDEXER_CHOICES,
        help_text="Escolha do indexador"
    )
    indexer = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Valor do Indexador",
        null=True, blank=True
    )
    real_tax = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Taxa real anual do produto",
        null=True,
        blank=True,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    minimum_value = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if (
            self.indexer is None
        ):
            if self.indexer_choice == IndexerEnum.SELIC.value:
                self.indexer = Decimal(get_selic_rate())
            elif self.indexer_choice == IndexerEnum.IPCA.value:
                self.indexer = Decimal(get_ipca_rate())

        if self.real_tax is None:
            self.real_tax = self.tax + self.indexer

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Investment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
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
        return f"Investimento de {self.account} no produto {self.product.name}"
