from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import Transaction
from account.models import Account
from .forms import TransactionForm 


class TransactionView(View):
    def get(self, request):
        from_account = request.user.account  
        
        transactions = Transaction.objects.filter(from_account=from_account) | Transaction.objects.filter(to_account=from_account)

        form = TransactionForm()
        return render(request, 'transaction_form.html', {'form': form, 'transactions': transactions})

    def post(self, request):
        form = TransactionForm(request.POST)
        
        if form.is_valid():
            # Conta de origem é a conta do usuário logado
            from_account = request.user  # Acesse a conta do usuário corretamente

            # Obtenha os dados do formulário
            to_account_cpf = form.cleaned_data['to_account']
            to_account = Account.objects.get(cpf=to_account_cpf)
            amount = form.cleaned_data['amount']

            # Validação de saldo
            if from_account.balance >= amount:
                # Crie a transação no banco de dados
                Transaction.objects.create(from_account=from_account, to_account=to_account, amount=amount)

                # Atualiza o saldo das contas
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()

                return redirect('home')  # Redirecionar após o sucesso
            else:
                # Adiciona um erro ao formulário se o saldo for insuficiente
                form.add_error('amount', 'Saldo insuficiente para realizar a transação.')

        return render(request, 'home.html', {'form': form})