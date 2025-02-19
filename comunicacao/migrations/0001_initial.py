# Generated by Django 4.2.19 on 2025-02-18 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=255, verbose_name='Nome do Usuário')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('senha', models.CharField(max_length=255, verbose_name='Senha')),
                ('data_cadastro', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de Cadastro')),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('departamento', models.CharField(max_length=100, unique=True, verbose_name='Departamento')),
                ('email_departamento', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail do Departamento')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['descricao'],
            },
        ),
        migrations.CreateModel(
            name='Reclamacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Em andamento', 'Em andamento'), ('Resolvido', 'Resolvido'), ('Cancelado', 'Cancelado')], max_length=50)),
                ('data_envio', models.DateField(auto_now_add=True, verbose_name='Data de Envio')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='reclamacoes/', verbose_name='Imagem')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='comunicacao.categoria', verbose_name='Categoria')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reclamacoes', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Reclamação',
                'verbose_name_plural': 'Reclamações',
            },
        ),
        migrations.CreateModel(
            name='ReclamacaoImagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='reclamacoes/', verbose_name='Imagem')),
                ('data_envio', models.DateTimeField(auto_now_add=True, verbose_name='Data de Envio')),
                ('reclamacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens', to='comunicacao.reclamacao', verbose_name='Reclamação')),
            ],
            options={
                'verbose_name': 'Imagem da Reclamação',
                'verbose_name_plural': 'Imagens das Reclamações',
            },
        ),
        migrations.CreateModel(
            name='HistoricoStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Em andamento', 'Em andamento'), ('Resolvido', 'Resolvido'), ('Cancelado', 'Cancelado')], max_length=50, verbose_name='Status')),
                ('data_alteracao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Alteração')),
                ('observacao', models.TextField(blank=True, null=True, verbose_name='Observação')),
                ('reclamacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico_status', to='comunicacao.reclamacao', verbose_name='Reclamação')),
            ],
            options={
                'verbose_name': 'Histórico de Status',
                'verbose_name_plural': 'Histórico de Status',
            },
        ),
    ]
