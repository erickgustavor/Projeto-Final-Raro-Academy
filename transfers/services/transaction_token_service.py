import os
import random
import string

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from caps_bank.tasks import celery_send_mail
from transfers.models import Transaction


class TransactionTokenService:
    def __init__(self, transaction_data):
        self.transaction_data = transaction_data
        self.token = None
        self.token_expiration = None

    def generate_token(self):

        self.token = "".join(random.choices(string.digits, k=6))
        expiration_minutes = int(os.getenv("TOKEN_EXPIRATION_MINUTES", 5))
        self.token_expiration = timezone.now() + timezone.timedelta(
            minutes=expiration_minutes
        )

        self.send_token_email()

    def send_token_email(self):

        subject = "Token para confirmação da transferência"
        message = f'Seu token de confirmação é: {self.token}. Ele expira em {self.token_expiration.strftime("%H:%M:%S")}.'
        recipient_email = self.transaction_data["from_account"].email
        if settings.USING_REDIS:
            celery_send_mail.delay(
                subject, message, "squadtech.capsbank@gmail.com", [recipient_email]
            )

        else:
            print("teste")
            send_mail(
                subject, message, "squadtech.capsbank@gmail.com", [recipient_email]
            )

    def confirm_transaction(self, token_input):

        if self.token_expiration <= timezone.now():
            return "O token expirou. Por favor, solicite um novo token."

        if self.token == token_input:

            transaction = Transaction(
                from_account=self.transaction_data["from_account"],
                to_account=self.transaction_data["to_account"],
                amount=self.transaction_data["amount"],
                token=self.token,
            )

            transaction.save()
            return "Transação confirmada com sucesso!"

        return "Token inválido. Por favor, verifique e tente novamente."
