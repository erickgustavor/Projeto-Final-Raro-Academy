from django.urls import path
from .views import registration_form, process_registration #, confirm_email

urlpatterns = [
    path('register/', registration_form, name='registration_form'),
    path('register/submit/', process_registration, name='process_registration')
    #URL para confirmar o email
]