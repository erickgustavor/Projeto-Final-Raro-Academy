from django.test import TestCase
from account.models import Account, RecoveryToken, AccountType
from uuid import uuid4

class AccountModelTests(TestCase):
    
    def setUp(self):
        self.account = Account.objects.create_user(
            email='test@example.com',
            username='testuser',
            cpf='115.006.346.70',
            password='password123'
        )

    def test_account_creation(self):
        self.assertEqual(self.account.email, 'test@example.com')
        self.assertEqual(self.account.username, 'testuser')
        self.assertEqual(self.account.cpf, '115.006.346.70')
        self.assertEqual(self.account.balance, 0.0)
        self.assertFalse(self.account.is_active)
        self.assertFalse(self.account.is_staff)
        self.assertEqual(self.account.type, AccountType.FREE)

    def test_str_method(self):
        self.assertEqual(str(self.account), 'test@example.com')

    def test_account_type_choices(self):
        self.assertIn((AccountType.FREE.value, AccountType.FREE.name.capitalize()), AccountType.choices())
        self.assertIn((AccountType.PREMIUM.value, AccountType.PREMIUM.name.capitalize()), AccountType.choices())
        self.assertIn((AccountType.ADMIN.value, AccountType.ADMIN.name.capitalize()), AccountType.choices())

class RecoveryTokenModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create_user(
        email='test@example.com',
        username='testuser',
        cpf='115.006.346.70',
        password='password123'
    )
        print("Account ID:", self.account.id)
        self.assertIsNotNone(self.account.id, "Account was not saved properly.")

        
    def test_recovery_token_creation(self):
        self.assertIsNotNone(self.account.id, "Account was not saved properly.")
        token = RecoveryToken.objects.create(account=self.account, value=str(uuid4()))
        self.assertIsNotNone(token.value)
        self.assertTrue(token.is_active)
        self.assertEqual(token.account, self.account)

    def test_token_string_representation(self):
        token = RecoveryToken.objects.create(account=self.account, value=str(uuid4()))
        self.assertIsInstance(token.value, str)
        self.assertGreater(len(token.value), 0)

    def test_token_activation(self):
        token = RecoveryToken.objects.create(account=self.account, value=str(uuid4()))
        token.is_active = False
        token.save()
        self.assertFalse(token.is_active)
