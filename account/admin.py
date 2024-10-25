from django.contrib import admin
from .models import Account


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
