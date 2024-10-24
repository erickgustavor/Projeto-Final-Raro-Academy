from django.urls import path

from .views import ConfirmView, LoginView, RegisterView, HomeView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("confirm/<int:account_id>/", ConfirmView.as_view(), name="confirm"),
    path("login/", LoginView.as_view(), name="login"),
    path("home/", HomeView.as_view(), name="home"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
