from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('account.urls')),
    path('transfers/', include('transfers.urls')),
    path('investments/', include('investments.urls')),
]
