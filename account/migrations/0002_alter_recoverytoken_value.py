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
