from enum import Enum
from django.db import models
from django.utils import timezone
from account.models import Account


class InvestmentRangeDateEnum(Enum):
    ONE_YEAR = 365
    ONE_MONTH = 30
    ONE_WEEK = 7


class Indexer(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class ProductInvestment(models.Model):
    name = models.CharField(max_length=100)
    tax = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Taxa anual do produto"
    )
    index_multiplier = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=1,
        help_text="Multiplicador do indexador"
    )
    indexer = models.ForeignKey(Indexer, on_delete=models.CASCADE)
    range_date = models.IntegerField(
        choices=[
            (InvestmentRangeDateEnum.ONE_YEAR.value, "1 ano"),
            (InvestmentRangeDateEnum.ONE_MONTH.value, "1 mês"),
            (InvestmentRangeDateEnum.ONE_WEEK.value, "1 semana"),
        ],
        default=InvestmentRangeDateEnum.ONE_YEAR.value,
    )
    start_date = models.DateField(auto_now_add=True)
    minimum_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

    def get_daily_tax(self):
        tax_daily = (
            (self.tax + (
                self.indexer.rate * self.index_multiplier
                )) / 365)/100
        return tax_daily


class Investment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInvestment, on_delete=models.CASCADE)
    applied_value = models.DecimalField(max_digits=10, decimal_places=2)
    accumulated_income = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    initial_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    rescue_data = models.DateField(null=True, blank=True)
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

    def update_income(self):
        print(self.product.get_daily_tax())
        self.accumulated_income += (
            self.applied_value + self.accumulated_income
        ) * self.product.get_daily_tax()
        print(self.accumulated_income)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.due_date = (
                timezone.now().date() + timezone.timedelta(
                    days=self.product.range_date
                ))
        super().save(*args, **kwargs)
