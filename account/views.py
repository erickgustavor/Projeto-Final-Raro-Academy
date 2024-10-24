from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from account.forms.login_forms import LoginForm
from account.forms.registration_forms import AccountRegistrationForm

from .models import Account


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
                f"http://{request.get_host()}/account/confirm/{account.id}/"
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = form.cleaned_data.get("email")

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
                    return redirect("login")

                login(request, account)
                return redirect("home")

        return redirect("login")


class LogoutView(View):
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


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")
