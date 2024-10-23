from django.contrib import admin
from .models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "begin", "end")
    search_fields = ("name",)
    fieldsets = (
        ("Informações da turma", {"fields": ["name", "icon"]}),
        (
            "Datas",
            {
                "fields": [
                    ("begin", "end"),
                ]
            },
        ),
        (
            "Participantes",
            {
                "fields": [
                    "accounts",
                ]
            },
        ),
    )
    filter_horizontal = ("accounts",)


admin.site.register(Group, GroupAdmin)
