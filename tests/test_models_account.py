from django.test import TestCase
from account.models import Account, AccountType

class AccountModelTestCase(TestCase):

    def setUp(self):
        self.account = Account.objects.create(
            username='testuser',
            password='plain_password',
            email='test@example.com',
            cpf='12345678901',
            balance=100.00,
            type=AccountType.FREE.value
        )

    def test_account_creation(self):
        self.assertEqual(self.account.username, 'testuser')
        self.assertEqual(self.account.email, 'test@example.com')
        self.assertEqual(self.account.cpf, '12345678901')
        self.assertEqual(self.account.balance, 100.00)
        self.assertEqual(self.account.type, AccountType.FREE.value)

    def test_password_is_hashed_on_save(self):
        self.assertNotEqual(self.account.password, 'plain_password')
        self.assertTrue(self.account.password.startswith('pbkdf2_sha256$'))

    def test_cpf_unique(self):
        with self.assertRaises(Exception):
            Account.objects.create(
                username='anotheruser',
                password='another_password',
                email='another@example.com',
                cpf='12345678901',
                balance=50.00,
                type=AccountType.PREMIUM.value
            )

    def test_str_method(self):
        self.assertEqual(str(self.account), 'testuser (Free)')


    def test_default_account_type(self):
        account = Account.objects.create(
            username='default_user',
            password='password',
            email='default@example.com',
            cpf='10987654321',
            balance=0.00
        )
        self.assertEqual(account.type, AccountType.FREE.value)
