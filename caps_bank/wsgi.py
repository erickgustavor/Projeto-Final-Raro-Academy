"""
WSGI config for caps_bank project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

from investments.tasks import update_cdi, update_selic, update_tjlp
from transfers.tasks import commit_transactions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caps_bank.settings")

if settings.USING_REDIS:
    update_selic.delay()
    update_tjlp.delay()
    update_cdi.delay()
    commit_transactions.delay()

application = get_wsgi_application()
