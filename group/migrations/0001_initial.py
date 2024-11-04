# Generated by Django 5.1.2 on 2024-11-03 22:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="nome"),
                ),
                ("icon", models.FileField(upload_to="icons/", verbose_name="ícone")),
                ("begin", models.DateField(verbose_name="data de ínicio")),
                ("end", models.DateField(verbose_name="data de fim")),
                (
                    "accounts",
                    models.ManyToManyField(
                        blank=True,
                        related_name="group",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="contas",
                    ),
                ),
            ],
        ),
    ]
