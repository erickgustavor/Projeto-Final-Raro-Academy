from datetime import datetime, time
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

from account.models import Account
from caps_bank.tasks import celery_send_mail
from transfers.models import Transaction
from transfers.services.transaction_token_service import TransactionTokenService

from .forms import TransactionForm
from .models import Transaction
from .services.commit_transactions_service import CommitTrasactionService


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
        token_expiration = timezone.datetime.strptime(
            request.session.get("token_expiration"), "%Y-%m-%d %H:%M:%S"
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

            commit_service = CommitTrasactionService(transaction)

            now = timezone.now()


            if 0 <= now.weekday() <= 4 and time(8, 0) <= now.time() <= time(18, 0):
                commit_service.make_transaction()
            else:
                transaction.is_committed = False

            transaction.save()

            request.session["success_message"] = "Transação confirmada com sucesso!"

            return redirect("home")
        else:
            return render(
                request,
                "confirm_transaction.html",
                {"error": "Token inválido. Verifique o token e tente novamente."},
            )
