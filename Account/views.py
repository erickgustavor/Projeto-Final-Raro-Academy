from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.core.mail import send_mail
from django.conf import settings
from account.forms.registration_forms import AccountRegistrationForm
from account.forms.login_forms import LoginForm
from .models import Account
from django.contrib import messages 

@require_GET
def login_view(request):
    form = LoginForm() 
    return render(request, 'login/login_form.html', {'form': form})

@require_POST
def login_process(request):
    form = LoginForm(request.POST)
    
    if form.is_valid():
        user = form.cleaned_data['user']  
        if user.is_active:
            request.session['user_id'] = user.id 
            return redirect('home') 
        else:
            messages.error(request, 'Por favor, confirme seu e-mail antes de fazer login.')
            return render(request, 'login/login_form.html', {'form': form})

    return render(request, 'login/login_form.html', {'form': form})

@require_GET
def registration_form(request):
    form = AccountRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@require_POST
def process_registration(request):
    form = AccountRegistrationForm(request.POST)

    if form.is_valid():
        account = form.save(commit=False)
        account.is_active = False 
        account.save()

        subject = 'Confirmação de Registro'
        message = 'Obrigado por se registrar! Por favor, ative sua conta clicando no link abaixo:\n\n' \
          f'http://{request.get_host()}/account/confirm/{account.id}/'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = form.cleaned_data.get('email')

        send_mail(subject, message, from_email, [to_email])

        return render(request, 'registration/confirmation_sent.html')

    return render(request, 'registration/register.html', {'form': form})

def confirm_registration(request, account_id):   
    
    account = get_object_or_404(Account, id=account_id)
    account.is_active = True
    account.save()

    return redirect('login_form')

@require_GET
def home_view(request):
    return render(request, 'home.html')
