from django.urls import path
from .views import registration_form, process_registration, confirm_registration, login_view, login_process, home_view

urlpatterns = [
    path('register/', registration_form, name='registration_form'),
    path('register/submit/', process_registration, name='process_registration'),
    path('confirm/<int:account_id>/', confirm_registration, name='confirm_registration'),
    path('login/', login_view, name='login_form'),
    path('login/process/', login_process, name='login_process'),
    path('home/', home_view, name='home')
]