# Generated by Django 5.1.2 on 2024-10-31 15:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0019_alter_productinvestment_final_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinvestment',
            name='final_date',
            field=models.DateField(default=datetime.datetime(2025, 1, 31, 15, 11, 30, 2208, tzinfo=datetime.timezone.utc)),
        ),
    ]
