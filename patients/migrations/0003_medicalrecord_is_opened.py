# Generated by Django 5.1.4 on 2025-01-24 00:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('patients', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalrecord',
            name='is_opened',
            field=models.BooleanField(default=True),
        ),
    ]
