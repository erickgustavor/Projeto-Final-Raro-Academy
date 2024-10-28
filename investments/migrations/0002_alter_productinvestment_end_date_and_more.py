# Generated by Django 5.1.2 on 2024-10-28 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("investments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productinvestment",
            name="end_date",
            field=models.DateField(verbose_name="data final"),
        ),
        migrations.AlterField(
            model_name="productinvestment",
            name="minimum_value",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="valor mínimo"
            ),
        ),
        migrations.AlterField(
            model_name="productinvestment",
            name="name",
            field=models.CharField(max_length=100, verbose_name="nome"),
        ),
        migrations.AlterField(
            model_name="productinvestment",
            name="start_date",
            field=models.DateField(verbose_name="data de início"),
        ),
        migrations.AlterField(
            model_name="productinvestment",
            name="tax",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Taxa anual do produto",
                max_digits=5,
                verbose_name="taxa anual",
            ),
        ),
    ]
