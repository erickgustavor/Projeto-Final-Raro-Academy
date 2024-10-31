from celery import shared_task
from caps_bank.tasks import celery_send_mail
from .models import Transaction


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def commit_transactions():
    transactions_uncommitted = Transaction.objects.filter(is_committed=False)
    for transaction in transactions_uncommitted:
        to_account = transaction.to_account
        from_account = transaction.from_account
        amount = transaction.amount
        if from_account.balance < amount:
            subject = "Transação recusada"
        from_account.balance -= amount
        to_account.balance += amount

        transaction.is_committed = True

        to_account.save()
        from_account.save()
        transaction.save()
