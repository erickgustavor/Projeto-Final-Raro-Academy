from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from account.forms import (
    AccountRegistrationForm,
    LoginForm,
    RecoveryPasswordConfirmForm,
    RecoveryPasswordRequestForm,
)
from caps_bank.tasks import celery_send_mail
from transfers.forms import TransactionForm
from transfers.models import Transaction

from .models import Account, RecoveryToken


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
            message = (
                "Obrigado por se registrar! Por favor, ative sua conta clicando no link abaixo:\n\n"
                f"http://{request.get_host()}/accounts/confirm/{account.id}/"
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = form.cleaned_data.get("email")

            if settings.USING_REDIS:
                celery_send_mail.delay(subject, message, from_email, [to_email])
            else:
                send_mail(subject, message, from_email, [to_email])

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
                messages.error(
                        request, "Informações inválidas."
                    )

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
            message = "O token para mudar de senha é:\n\n" f"{token.value}"
            from_email = settings.DEFAULT_FROM_EMAIL

            if settings.USING_REDIS:
                celery_send_mail.delay(subject, message, from_email, [to_email])
            else:
                send_mail(subject, message, from_email, [to_email])
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
            from_account=request.user
        ) | Transaction.objects.filter(to_account=request.user)

        return render(
            request,
            "home.html",
            {
                "form": form,
                "transactions": transactions,
                "balance": request.user.balance,
            },
        )
