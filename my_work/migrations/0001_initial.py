# Generated by Django 4.1.5 on 2024-07-18 11:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Username must contain only letters, numbers, and @/./+/-/_ characters.', regex='^[\\w.@+-]+$')])),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user_type', models.CharField(blank=True, choices=[('staff', 'staff'), ('exicutive', 'exicutive')], max_length=20, null=True)),
                ('address', models.TextField(null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeneralHolidays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('speciality', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+91XXXXXXXXXX' and must be exactly 14 characters long.", regex='^\\+91\\d{10}$')])),
                ('date_of_birth', models.DateField(null=True)),
                ('permenant_address', models.TextField()),
                ('current_address', models.TextField()),
                ('qualification', models.CharField(max_length=200, null=True)),
                ('bank_name', models.CharField(max_length=200, null=True)),
                ('ac_no', models.PositiveIntegerField(null=True)),
                ('ifsc_code', models.CharField(max_length=15, null=True)),
                ('branch', models.CharField(max_length=100, null=True)),
                ('age', models.PositiveBigIntegerField()),
                ('father_name', models.CharField(max_length=50)),
                ('mothers_name', models.CharField(max_length=50)),
                ('spouse_name', models.CharField(max_length=50, null=True)),
                ('married', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
                ('status1', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('reason', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendancedb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('checkin', models.TimeField(null=True)),
                ('checkout', models.TimeField(null=True)),
                ('start', models.BooleanField(default=False)),
                ('end', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
