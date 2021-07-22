# Generated by Django 3.2.5 on 2021-07-22 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('IATA', models.CharField(max_length=5)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
