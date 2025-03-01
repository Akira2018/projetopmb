# Generated by Django 5.0.7 on 2024-12-14 19:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_customuser_telefone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='telefone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='O telefone deve estar no formato (XX) XXXXX-XXXX.', regex='^\\(\\d{2}\\) \\d{4,5}-\\d{4}$')], verbose_name='Telefone'),
        ),
    ]
