import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='created_at',
            field=models.DateField(
                auto_now_add=True,
                verbose_name='Создано',
                default=datetime.date(2025, 8, 10),
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='habit',
            name='last_reminded_at',
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name='Последнее напоминание',
            ),
        ),
    ]
