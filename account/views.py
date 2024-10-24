from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from account.forms.login_forms import LoginForm
from account.forms.registration_forms import AccountRegistrationForm

from .models import Account


@require_GET
def login_view(request):
    form = LoginForm()
    return render(request, "login/login_form.html", {"form": form})


@require_POST
def login_process(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        if not Account.objects.filter(email=email).exists():
            messages.error(request, "Conta não cadastrada.")
            return redirect("registration_form")

        account = authenticate(request, email=email, password=password)

        if account:
            if not account.is_active:
                messages.error(
                    request, "Por favor, confirme seu e-mail antes de fazer login."
                )
                return redirect("login_form")

            login(request, account)
            return redirect("home")

    return redirect("login_form")


@require_GET
def registration_form(request):
    form = AccountRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@require_POST
def process_registration(request):
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


def confirm_registration(request, account_id):

    account = get_object_or_404(Account, id=account_id)
    account.is_active = True
    account.save()

    return redirect("login_form")


@require_GET
def home_view(request):
    return render(request, "home.html")
