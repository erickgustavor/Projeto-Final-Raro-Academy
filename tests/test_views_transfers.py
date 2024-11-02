from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from account.models import Account
from transfers.models import Transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password',
            email='user@example.com',
            cpf='12345678901'
        )
        self.other_user = User.objects.create_user(
            username='testuser2',
            password='password',
            email='other@example.com',
            cpf='12345678902'
        )

        self.user_account = Account.objects.create(
            user=self.user,
            cpf="12345678901", 
            email="user@example.com", 
            balance=100.00
        )
        self.other_account = Account.objects.create(
            user=self.other_user,
            cpf="12345678902", 
            email="other@example.com", 
            balance=50.00
        )

        self.client.login(username='testuser', password='password')

    def test_transaction_view_valid_post(self):
        response = self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })

        self.assertRedirects(response, reverse('confirm_transaction'))

        self.assertIn('transaction_token', self.client.session)
        self.assertIn('transaction_data', self.client.session)

    def test_transaction_view_insufficient_balance(self):
        response = self.client.post(reverse('transaction'), {
            'amount': 200.00,
            'to_account': self.other_account.id,
        })

        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, "Saldo insuficiente para realizar a transação.")

    def test_confirm_transaction_view_valid_post(self):
        self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })

        transaction_token = self.client.session["transaction_token"]
        response = self.client.post(reverse('confirm_transaction'), {
            'token': transaction_token,
        })

        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, "Transação confirmada com sucesso!")
        self.assertEqual(Transaction.objects.count(), 1)

    def test_confirm_transaction_view_invalid_token(self):
        self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })

        response = self.client.post(reverse('confirm_transaction'), {
            'token': 'invalid_token',
        })

        self.assertTemplateUsed(response, 'confirm_transaction.html')
        self.assertContains(response, "Token inválido. Verifique o token e tente novamente.")

    def test_confirm_transaction_view_expired_token(self):
        self.client.post(reverse('transaction'), {
            'amount': 10.00,
            'to_account': self.other_account.id,
        })

        self.client.session['token_expiration'] = (timezone.now() - timezone.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

        response = self.client.post(reverse('confirm_transaction'), {
            'token': self.client.session["transaction_token"],
        })

        self.assertTemplateUsed(response, 'confirm_transaction.html')
        self.assertContains(response, "O token expirou. Solicite uma nova transação.")
