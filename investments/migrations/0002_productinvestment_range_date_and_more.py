# Generated by Django 5.1.2 on 2024-10-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinvestment',
            name='range_date',
            field=models.IntegerField(choices=[(365, '1 ano'), (30, '1 mês'), (7, '1 semana')], default=365),
        ),
        migrations.AlterField(
            model_name='productinvestment',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
