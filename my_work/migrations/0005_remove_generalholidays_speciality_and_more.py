# Generated by Django 4.1.5 on 2024-07-20 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_work', '0004_alter_generalholidays_speciality'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalholidays',
            name='speciality',
        ),
        migrations.AddField(
            model_name='generalholidays',
            name='reason',
            field=models.TextField(null=True),
        ),
    ]
