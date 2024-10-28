from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.utils import timezone
from django.core.mail import send_mail
from .models import Transaction
from account.models import Account
from transfers.models import Transaction
from .forms import TransactionForm
from transfers.services.transaction_token_service import TransactionTokenService
from decimal import Decimal


class TransactionView(View):
    def get(self, request):
        from_account = request.user.account  
        
        transactions = Transaction.objects.filter(from_account=from_account) | Transaction.objects.filter(to_account=from_account)

        form = TransactionForm()
        return render(request, 'transaction_form.html', {'form': form, 'transactions': transactions})

    def post(self, request):
        form = TransactionForm(request.POST)
        
        if form.is_valid():
            from_account = request.user  
            to_account_cpf = form.cleaned_data['to_account']
            to_account = Account.objects.get(cpf=to_account_cpf)
            amount = form.cleaned_data['amount']

            if from_account.balance >= amount:

                transaction_data = {
                    'from_account': from_account,
                    'to_account': to_account.id,
                    'amount': float(amount)
                }
                token_service = TransactionTokenService(transaction_data)
                token_service.generate_token()

                request.session['transaction_data'] = {
                    'from_account_id': from_account.id,
                    'to_account_id': to_account.id,
                    'amount': float(amount)
                }
                request.session['transaction_token'] = token_service.token
                request.session['token_expiration'] = token_service.token_expiration.strftime("%Y-%m-%d %H:%M:%S")

                return redirect('confirm_transaction')  
            else:
                form.add_error('amount', 'Saldo insuficiente para realizar a transação.')

        return render(request, 'home.html', {'form': form})
    

class ConfirmTransactionView(View):
    def get(self, request):

        return render(request, 'confirm_transaction.html')

    def post(self, request):
        token_input = request.POST.get('token')
        transaction_data = request.session.get('transaction_data')
        token = request.session['transaction_token']
        token_expiration = timezone.make_aware(timezone.datetime.strptime(request.session.get('token_expiration'), "%Y-%m-%d %H:%M:%S"))

        if timezone.now() > token_expiration:
            return render(request, 'confirm_transaction.html', {'error': 'O token expirou. Solicite uma nova transação.'})

        if token == token_input:
            from_account = Account.objects.get(id=transaction_data['from_account_id'])
            to_account = Account.objects.get(id=transaction_data['to_account_id'])
            amount = Decimal(transaction_data['amount'])

            transaction = Transaction(from_account=from_account, to_account=to_account, amount=amount, token=token)
            transaction.save()

            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            send_mail(
                'Transação Confirmada',
                f'Sua transação de R$ {amount:.2f} para {to_account.username} (CPF {to_account.cpf}) foi realizada com sucesso.',
                settings.DEFAULT_FROM_EMAIL,
                [from_account.email],
                fail_silently=False,
            )

            send_mail(
                'Você recebeu uma transação',
                f'Você recebeu R$ {amount:.2f} de {from_account.username} (CPF {from_account.cpf}).',
                settings.DEFAULT_FROM_EMAIL,
                [to_account.email],
                fail_silently=False,
            )

            request.session['success_message'] = "Transação confirmada com sucesso!"
            return redirect('home')
        else:
            return render(request, 'confirm_transaction.html', {'error': 'Token inválido. Verifique o token e tente novamente.'})