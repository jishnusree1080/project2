# Generated by Django 4.1.5 on 2024-07-22 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_work', '0009_alter_dailyupdatemodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveupdate',
            name='created_at',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]