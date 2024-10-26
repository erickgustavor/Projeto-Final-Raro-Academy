from django.shortcuts import render
from .models import ProductInvestment


def product_list(request):
    products = ProductInvestment.objects.all()
    context = {
        "products": products,
    }
    return render(request, "product_list.html", context)
