# Generated by Django 5.1.2 on 2024-10-28 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("investments", "0002_alter_productinvestment_end_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productinvestment",
            name="is_premium",
            field=models.BooleanField(default=False, verbose_name="premium"),
        ),
    ]
