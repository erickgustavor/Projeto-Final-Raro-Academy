# Generated by Django 5.1.2 on 2024-10-22 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Account", "0002_alter_account_cpf_alter_account_email_and_more"),
        ("group", "0003_alter_group_accounts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="accounts",
            field=models.ManyToManyField(
                blank=True,
                related_name="group",
                to="Account.account",
                verbose_name="contas",
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="begin",
            field=models.DateField(verbose_name="data de ínicio"),
        ),
        migrations.AlterField(
            model_name="group",
            name="end",
            field=models.DateField(verbose_name="data de fim"),
        ),
        migrations.AlterField(
            model_name="group",
            name="icon",
            field=models.FileField(upload_to="icons/", verbose_name="ícone"),
        ),
        migrations.AlterField(
            model_name="group",
            name="name",
            field=models.CharField(max_length=100, unique=True, verbose_name="nome"),
        ),
    ]
