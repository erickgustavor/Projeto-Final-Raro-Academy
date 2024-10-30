from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from account.models import Account
from transfers.models import Transaction
from transfers.services.transaction_token_service import TransactionTokenService
from .forms import TransactionForm
from .models import Transaction
from django.template.loader import render_to_string


class TransactionView(LoginRequiredMixin, View):
    def post(self, request):
        form = TransactionForm(request.POST, user=request.user)

        if form.is_valid():
            from_account = request.user
            to_account = form.cleaned_data["to_account"]
            amount = form.cleaned_data["amount"]

            if from_account.balance >= amount:

                transaction_data = {
                    "from_account": from_account,
                    "to_account": to_account.id,
                    "amount": float(amount),
                }
                token_service = TransactionTokenService(transaction_data)
                token_service.generate_token()

                request.session["transaction_data"] = {
                    "from_account_id": from_account.id,
                    "to_account_id": to_account.id,
                    "amount": float(amount),
                }
                request.session["transaction_token"] = token_service.token
                request.session["token_expiration"] = (
                    token_service.token_expiration.strftime("%Y-%m-%d %H:%M:%S")
                )

                return redirect("confirm_transaction")
            else:
                form.add_error(None, "Saldo insuficiente para realizar a transação.")

        for error in form.non_field_errors():
            messages.error(request, error)

        return redirect("home")


class ConfirmTransactionView(LoginRequiredMixin, View):
    def get(self, request):

        return render(request, "confirm_transaction.html")

    def post(self, request):
        token_input = request.POST.get("token")
        transaction_data = request.session.get("transaction_data")
        token = request.session["transaction_token"]
        token_expiration = timezone.make_aware(
            timezone.datetime.strptime(
                request.session.get("token_expiration"), "%Y-%m-%d %H:%M:%S"
            )
        )

        if timezone.now() > token_expiration:
            return render(
                request,
                "confirm_transaction.html",
                {"error": "O token expirou. Solicite uma nova transação."},
            )

        if token == token_input:
            from_account = Account.objects.get(id=transaction_data["from_account_id"])
            to_account = Account.objects.get(id=transaction_data["to_account_id"])
            amount = Decimal(transaction_data["amount"])

            transaction = Transaction(
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                token=token,
            )
            transaction.save()

            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            subject = "Transação Confirmada"
            html_content = render_to_string("email/transaction_confirmed.html", {
                "from_account": from_account,
                "to_account": to_account,
                "amount": amount
            })
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = [from_account.email]

            email = EmailMultiAlternatives(subject, html_content, email_from, email_to)
            email.attach_alternative(html_content, "text/html")
            email.send()

            
            subject = "Você recebeu uma transação"
            html_content = render_to_string("email/transaction_received.html", {
                "from_account": from_account,
                "to_account": to_account,
                "amount": amount
            })
            email_to = [to_account.email]

            email = EmailMultiAlternatives(subject, html_content, email_from, email_to)
            email.attach_alternative(html_content, "text/html")
            email.send()

            request.session["success_message"] = "Transação confirmada com sucesso!"
            
            return redirect("home")
        else:
            return render(
                request,
                "confirm_transaction.html",
                {"error": "Token inválido. Verifique o token e tente novamente."},
            )
