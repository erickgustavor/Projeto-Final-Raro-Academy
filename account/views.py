from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

from account.forms import (
    AccountRegistrationForm,
    LoginForm,
    RecoveryPasswordConfirmForm,
    RecoveryPasswordRequestForm,
)
from caps_bank.tasks import celery_send_mail
from investments.models import Investment
from transfers.forms import TransactionForm
from transfers.models import Transaction

from .models import Account, Deposit, RecoveryToken


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = AccountRegistrationForm()
        return render(request, "registration/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AccountRegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            cpf = form.cleaned_data.get("cpf")
            password = form.cleaned_data.get("password")

            account = Account.objects.create_user(
                username=username, email=email, cpf=cpf, password=password
            )
            account.is_active = False
            account.save()

            subject = "Confirmação de Registro"

            html_content = render_to_string(
                "email/registration_confirmation.html",
                {
                    "username": username,
                    "confirmation_link": f"http://{request.get_host()}/accounts/confirm/{account.id}/",
                },
            )

            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = email

            if settings.USING_REDIS:
                celery_send_mail.delay(subject, html_content, from_email, to_email)
            else:
                celery_send_mail(subject, html_content, from_email, to_email)

            return render(request, "registration/confirmation_sent.html")

        return render(request, "registration/register.html", {"form": form})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "login/login_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            if not Account.objects.filter(email=email).exists():
                messages.error(request, "Conta não cadastrada.")
                return redirect("register")

            account = authenticate(request, email=email, password=password)

            if account:
                if not account.is_active:
                    messages.error(
                        request, "Por favor, confirme seu e-mail antes de fazer login."
                    )

                login(request, account)
                return redirect("home")
            else:
                messages.error(request, "Informações inválidas.")

        return redirect("login")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect("login")


class ConfirmView(View):
    def get(request, *args, **kwargs):
        account_id = kwargs["account_id"]

        account = get_object_or_404(Account, id=account_id)
        account.is_active = True
        account.save()

        return redirect("login")


class RecoveryPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "registration/recovery_password.html",
            {
                "request_form": RecoveryPasswordRequestForm(),
                "confirm_form": RecoveryPasswordConfirmForm(),
            },
        )

    def post(self, request, *args, **kwargs):
        form = RecoveryPasswordRequestForm(data=request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get("email")
            account = Account.objects.get(email=to_email)

            token = RecoveryToken(account=account)
            token.save()

            subject = "Recuperação de Senha"
            from_email = settings.DEFAULT_FROM_EMAIL

            html_content = render_to_string(
                "email/recovery_password.html",
                {
                    "account": account,
                    "token": token.value,
                },
            )

            if settings.USING_REDIS:
                celery_send_mail.delay(subject, html_content, from_email, to_email)
            else:
                celery_send_mail(subject, html_content, from_email, to_email)
            messages.info(request, "O token foi enviado pelo email.")

            return redirect("password-recovery")

        return render(
            request,
            "registration/recovery_password.html",
            {
                "request_form": form,
                "confirm_form": RecoveryPasswordConfirmForm(),
            },
        )


class RecoveryPasswordConfirmView(View):
    def post(self, request, *args, **kwargs):
        form = RecoveryPasswordConfirmForm(data=request.POST)
        if form.is_valid():
            token_value = form.cleaned_data.get("token")
            token = RecoveryToken.objects.get(value=token_value)
            password = form.cleaned_data.get("password")

            token_age = timezone.now() - token.created_at

            if token_age < timedelta(hours=2):
                account = token.account
                account.set_password(password)
                account.save()
                token.delete()
                messages.success(request, "A senha foi alterada com sucesso.")
                return redirect("login")

            messages.error("O código expirou, solicite outro código.")

        for error in form.non_field_errors():
            messages.error(request, error)
        return redirect("password-recovery")


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TransactionForm(user=request.user)

        transactions = Transaction.objects.filter(
            from_account=request.user, is_committed=True
        )

        return render(
            request,
            "home.html",
            {
                "form": form,
                "transactions": transactions,
                "balance": request.user.balance,
            },
        )


class ExtractView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        account = request.user
        data = []

        transactions_from = [
            {"type": "transaction", "timestamp": timestamp, "amount": -amount}
            for timestamp, amount in Transaction.objects.filter(
                from_account=account, is_committed=True
            ).values_list("timestamp", "amount")
        ]
        transactions_to = [
            {"type": "transaction", "timestamp": timestamp, "amount": amount}
            for timestamp, amount in Transaction.objects.filter(
                to_account=account, is_committed=True
            ).values_list("timestamp", "amount")
        ]
        deposits = [
            {"type": "deposit", "timestamp": timestamp, "amount": amount}
            for timestamp, amount in Deposit.objects.filter(
                to_account=account
            ).values_list("timestamp", "amount")
        ]
        investments = [
            {
                "type": "investments",
                "timestamp": rescue_date,
                "amount": applied_value + accumulated_income,
            }
            for applied_value, accumulated_income, rescue_date in Investment.objects.filter(
                account=account, status__in=["resgatado", "vencido"]
            ).values_list(
                "applied_value", "accumulated_income", "rescue_date"
            )
        ]

        data = sorted(
            transactions_from + transactions_to + deposits + investments,
            key=lambda x: x["timestamp"],
            reverse=True,
        )

        return render(
            request,
            "extract.html",
            {"infos": data},
        )
