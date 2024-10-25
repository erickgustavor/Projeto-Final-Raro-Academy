from django.shortcuts import render, redirect
from django.views import View
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

            from_account = request.user  

           
            to_account_cpf = form.cleaned_data['to_account']
            to_account = Account.objects.get(cpf=to_account_cpf)
            amount = form.cleaned_data['amount']

            
            if from_account.balance >= amount:
                
                Transaction.objects.create(from_account=from_account, to_account=to_account, amount=amount)

                
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()

                return redirect('home')  
            else:
                
                form.add_error('amount', 'Saldo insuficiente para realizar a transação.')

        return render(request, 'home.html', {'form': form})