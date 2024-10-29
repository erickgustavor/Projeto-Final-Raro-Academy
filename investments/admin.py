from django.contrib import admin
from .models import ProductInvestment, Investment


class ProductInvestmentAdmin(admin.ModelAdmin):
    list_display = (
        "name", "tax", "indexer_choice",
        "indexer", "start_date", "end_date", "minimum_value")


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ("product", "applied_value", "investment_data", "status")


admin.site.register(ProductInvestment, ProductInvestmentAdmin)
admin.register(Investment, InvestmentAdmin)
