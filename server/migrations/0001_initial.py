# Generated by Django 3.2.5 on 2021-07-26 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(help_text='이메일', max_length=100, unique=True, verbose_name='Email')),
                ('password', models.CharField(help_text='비밀번호', max_length=128, null=True, verbose_name='password')),
                ('phone', models.CharField(help_text='전화번호', max_length=15, null=True, verbose_name='phone')),
                ('passport', models.BooleanField(default=False, help_text='여권', verbose_name='passport')),
                ('provider', models.CharField(default='DEFAULT', help_text='DEFAULT | APPLE | GOOGLE | KAKAO', max_length=20, verbose_name='provider')),
                ('token', models.CharField(help_text='Refresh Token', max_length=255, null=True, verbose_name='token')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='공항명', max_length=100, verbose_name='공항명')),
                ('country', models.CharField(help_text='국가', max_length=100, verbose_name='국가')),
                ('IATA', models.CharField(help_text='IATA', max_length=5, verbose_name='IATA')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
