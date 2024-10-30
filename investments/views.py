from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import ProductInvestment, Investment
from .forms import InvestmentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = ProductInvestment.objects.all()
        context = {
            "products": products,
        }
        return render(request, "product_list.html", context)


class ProductDetailView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(ProductInvestment, id=product_id)
        context = {
            "product": product,
        }
        return render(request, "product_detail.html", context)


class InvestmentCreateView(LoginRequiredMixin, View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(ProductInvestment, id=product_id)
        form = InvestmentForm()
        context = {
            "form": form,
            "product": product,
        }
        return render(request, "investment_form.html", context)

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(ProductInvestment, id=product_id)
        form = InvestmentForm(request.POST)
        context = {
            "form": form,
            "product": product,
        }

        if not form.is_valid():
            messages.error(
                request, "Dados inválidos. Por favor, verifique o formulário."
            )
            return render(request, "investment_form.html", context)

        applied_value = form.cleaned_data.get("applied_value")
        account = request.user

        if applied_value < product.minimum_value:
            messages.error(
                request,
                """O valor de aplicação não pode ser
                menor que o valor mínimo do produto.""",
            )
            return render(request, "investment_form.html", context)

        if applied_value > account.balance:
            messages.error(
                request, "Saldo insuficiente para realizar este investimento."
            )
            return render(request, "investment_form.html", context)

        Investment.objects.create(
            account=account,
            product=product,
            applied_value=applied_value,
        )

        account.balance -= applied_value
        account.save()

        messages.success(request, "Investimento contratado com sucesso!")
        return redirect("my_investments")


class MyInvestmentsListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        investments = Investment.objects.filter(account=request.user)
        context = {
            "investments": investments,
        }
        return render(request, "my_investments.html", context)
