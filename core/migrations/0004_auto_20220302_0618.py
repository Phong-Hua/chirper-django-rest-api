# Generated by Django 2.2 on 2022-03-02 06:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20220302_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=255, unique=True, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
