# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator  # Adicionada a importação

class Usuario(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

class CustomUser(AbstractUser):
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone",
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
                message="O telefone deve estar no formato (XX) XXXXX-XXXX."
            )
        ]
    )
    membro_da_equipe = models.BooleanField(default=False, verbose_name="Membro da equipe")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="customuser_usuarios_set",  # Evitar conflito de user_set
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="customuser_usuarios_permissions",  # Evitar conflito de user_set
        blank=True
    )

    def __str__(self):
        return self.username






