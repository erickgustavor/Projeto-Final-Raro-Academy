import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recoverytoken',
            name='value',
            field=models.CharField(default=uuid.uuid4, max_length=200),
        ),
    ]
