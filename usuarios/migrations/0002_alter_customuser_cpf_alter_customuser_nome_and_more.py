# Generated by Django 5.0.7 on 2024-11-28 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nome',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome Completo'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='telefone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone'),
        ),
    ]
