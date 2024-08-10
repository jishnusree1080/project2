# Generated by Django 4.1.5 on 2024-08-05 05:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_work', '0013_expencemodel_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='expencemodel',
            name='others',
            field=models.FileField(blank=True, null=True, upload_to='poster/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'png'])]),
        ),
    ]