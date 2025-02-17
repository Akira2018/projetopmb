from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model  # Corrija a importação
from django.conf import settings  # Import necessário
from django.core.mail import send_mail
from django.core.mail import send_mail, BadHeaderError
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage

# Modelo de Administrador
class Admin(models.Model):
    usuario = models.CharField(max_length=255, verbose_name="Nome do Usuário")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    senha = models.CharField(max_length=255, verbose_name="Senha")
    data_cadastro = models.DateTimeField(default=now, verbose_name="Data de Cadastro")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

# Modelo de Categoria
class Categoria(models.Model):
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    departamento = models.CharField(max_length=100, unique=True, verbose_name="Departamento")
    email_departamento = models.EmailField(blank=True, null=True, verbose_name="E-mail do Departamento")

    def __str__(self):
        return self.descricao  # Agora apenas a descrição será exibida

    class Meta:
        ordering = ['descricao']  # Ordena as categorias alfabeticamente
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Reclamacao(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em andamento', 'Em andamento'),
        ('Resolvido', 'Resolvido'),
        ('Cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="reclamacoes",
        verbose_name="Usuário"
    )
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.ForeignKey(
        'Categoria', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria"
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    data_envio = models.DateField(auto_now_add=True, verbose_name="Data de Envio")
    imagem = models.ImageField(upload_to='reclamacoes/', null=True, blank=True, verbose_name="Imagem")  # Novo campo para imagem

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        status_anterior = None
        if self.pk:  # Verifica se a reclamação já existe
            reclamacao_anterior = Reclamacao.objects.get(pk=self.pk)
            status_anterior = reclamacao_anterior.status

        super().save(*args, **kwargs)  # Salva a reclamação normalmente

        # Registra histórico se o status mudou
        if status_anterior != self.status:
            HistoricoStatus.objects.create(
                reclamacao=self,
                status=self.status,
                observacao=f"Status alterado para {self.status} durante o envio de notificação."
            )

        # Verifica se há uma categoria com um e-mail associado
        if self.categoria and self.categoria.email_departamento:
            try:
                assunto = f"Nova Notificação: {self.titulo}"
                mensagem = f"""
                    Detalhes da Notificação:
                    Usuário: {self.usuario}
                    Título: {self.titulo}
                    Descrição: {self.descricao}
                    Categoria: {self.categoria.departamento}
                    Data de Envio: {self.data_envio}

                    Estamos enviando essa notificação através do aplicativo "Gestão de Relacionamentos".  
                    Por favor, tome as providências necessárias.

                    Atenciosamente,  
                    Sistema de Notificações
                """

                # Criação do e-mail
                email = EmailMessage(
                    subject=assunto,
                    body=mensagem,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[self.categoria.email_departamento],
                )

                # Verifica se há uma imagem anexada à reclamação
                if self.imagem and default_storage.exists(self.imagem.name):
                    with default_storage.open(self.imagem.name, 'rb') as f:
                        email.attach(self.imagem.name, f.read(), 'image/jpeg')  # Tipo MIME ajustado para JPEG

                # Envia o e-mail
                email.send(fail_silently=False)

            except BadHeaderError:
                pass  # Captura erros de cabeçalho de e-mail

    class Meta:
        verbose_name = "Reclamação"
        verbose_name_plural = "Reclamações"

# Histórico de Status
class HistoricoStatus(models.Model):
    reclamacao = models.ForeignKey(
        Reclamacao, on_delete=models.CASCADE, related_name="historico_status", verbose_name="Reclamação"
    )
    status = models.CharField(
        max_length=50,
        choices=Reclamacao.STATUS_CHOICES,  # Usa as opções de status do modelo Reclamacao
        verbose_name="Status"
    )
    data_alteracao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Alteração")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")

    def __str__(self):
        return f"Histórico - {self.reclamacao.titulo} - {self.status}"

    class Meta:
        verbose_name = "Histórico de Status"
        verbose_name_plural = "Histórico de Status"

class ReclamacaoImagem(models.Model):
    reclamacao = models.ForeignKey(
        Reclamacao, on_delete=models.CASCADE, related_name="imagens", verbose_name="Reclamação"
    )
    imagem = models.ImageField(upload_to="reclamacoes/", verbose_name="Imagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")

    def __str__(self):
        return f"Imagem de {self.reclamacao.titulo}"

    class Meta:
        verbose_name = "Imagem da Reclamação"
        verbose_name_plural = "Imagens das Reclamações"




