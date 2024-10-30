from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True, max_retries=3, default_retry_delay=60)  
def celery_send_mail(subject, message, from_email, to_email):
    send_mail(subject, message, from_email, to_email)
