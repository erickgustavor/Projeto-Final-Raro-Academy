"""
WSGI config for caps_bank project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from investments.tasks import update_selic


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caps_bank.settings')

update_selic.delay()

application = get_wsgi_application()

