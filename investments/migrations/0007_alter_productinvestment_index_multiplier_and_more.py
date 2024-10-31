# Generated by Django 5.1.2 on 2024-10-30 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("investments", "0006_alter_indexer_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productinvestment",
            name="index_multiplier",
            field=models.DecimalField(
                decimal_places=2,
                default=1,
                help_text="Multiplicador do indexador",
                max_digits=5,
                verbose_name="Multiplicador do indexador",
            ),
        ),
        migrations.AlterField(
            model_name="productinvestment",
            name="tax",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Taxa anual do produto",
                max_digits=5,
                verbose_name="taxa administrativa anual",
            ),
        ),
    ]
