# Generated by Django 2.2 on 2022-03-02 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatarURL',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
