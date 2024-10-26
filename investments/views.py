from django.shortcuts import render
from django.views import View
from .models import ProductInvestment


class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = ProductInvestment.objects.all()
        context = {"products": products}
        return render(request, "product_list.html", context)
