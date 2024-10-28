from django.contrib import admin

from .models import ProductInvestment


@admin.register(ProductInvestment)
class ProductInvestmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tax",
        "start_date",
        "end_date",
        "minimum_value",
        "is_premium",
    )
    search_fields = ("name", "minimum_value")
    fieldsets = (
        ("Informações do Produto", {"fields": ["name", "tax"]}),
        (
            "Datas",
            {
                "fields": [
                    ("start_date", "end_date"),
                ]
            },
        ),
        (None, {"fields": ["minimum_value", "is_premium"]}),
    )
