from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import Account
from django.db.models import Sum
from investments.models import  Investment

class AccountAdmin(admin.ModelAdmin):
    list_display = ("username", "type", "balance", "display_groups")
    search_fields = ("username",)
    readonly_fields = ("display_groups", "type")
    fieldsets = (
        (None, {"fields": ["username", "type", "display_groups"]}),
        (None, {"fields": ["balance"]}),
    )

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.group.all()])

    display_groups.short_description = "Turmas"

admin.site.register(Account, AccountAdmin)

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):

        default_urls = super().get_urls()  

        custom_urls = [
            path("", self.admin_view(self.dashboard_view), name="dashboard"),
        ]
        return custom_urls + default_urls

    def dashboard_view(self, request):

        total_active_users = Account.objects.filter(is_active=True).count()
        premium_users = Account.objects.filter(type='premium').count()
        total_invested = Investment.objects.aggregate(total=Sum('applied_value'))['total'] or 0

        context = dict(
            self.each_context(request),
            total_active_users=total_active_users,
            premium_users=premium_users,
            total_invested=total_invested,
        )
        return TemplateResponse(request, "admin/custom_dashboard.html", context)


custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(Account, AccountAdmin)
admin.site = custom_admin_site