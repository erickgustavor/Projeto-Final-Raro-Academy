from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from .forms import AccountRegistrationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from .validations import validate_cpf, validate_email, validate_username


@require_GET
def registration_form(request):
    form = AccountRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@require_POST
def process_registration(request):
    form = AccountRegistrationForm(request.POST)

    if form.is_valid():
        cpf = form.cleaned_data.get('cpf')
        try:
            validate_cpf(cpf)
        except ValidationError as e:
            messages.error(request, str(e.message))
            return render(request, 'registration/register.html', {'form': form})

        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')

        try:
            validate_username(username)  
            validate_email(email)
        except ValidationError as e:
            messages.error(request, str(e.message))
            return render(request, 'registration/register.html', {'form': form})

        account = form.save(commit=False)
        account.is_active = False
        account.save()

        # Chama a função para enviar o e-mail de confirmação

        return render(request, 'registration/confirmation_sent.html')

    return render(request, 'registration/register.html', {'form': form})
