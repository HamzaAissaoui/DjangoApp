# Generated by Django 3.2.13 on 2022-05-17 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0002_alter_provider_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='email',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]