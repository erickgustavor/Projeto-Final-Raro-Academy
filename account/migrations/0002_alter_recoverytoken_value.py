<<<<<<< HEAD
# Generated by Django 5.1.2 on 2024-10-31 02:09
=======
# Generated by Django 5.1.2 on 2024-10-31 00:10
>>>>>>> develop

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recoverytoken',
            name='value',
            field=models.CharField(max_length=9, unique=True),
        ),
    ]
