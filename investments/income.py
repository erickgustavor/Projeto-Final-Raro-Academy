from django.utils import timezone
from decimal import Decimal


def calculate_daily_income(applied_value, real_tax):
    daily_rate = (real_tax / Decimal(365)) / Decimal(100)
    daily_income = applied_value * daily_rate
    return daily_income


def redeem_investment(investment):
    if investment.product.end_date < timezone.now().date():
        investment.status = "resgatado"
        investment.rescue_data = timezone.now()
        investment.save()
        return investment.applied_value + investment.accumulated_income
    return 0


def update_income(investment):
    real_tax = investment.product.real_tax
    daily_income = calculate_daily_income(investment.applied_value, real_tax)
    investment.accumulated_income += daily_income
    investment.save()
