from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Reclamacao, HistoricoStatus
from django.core.mail import send_mail
from django.db.models.signals import pre_save

@receiver(post_save, sender=Reclamacao)
def enviar_email_reclamacao(sender, instance, created, **kwargs):
    """ Enviar e-mail automaticamente após registrar uma nova reclamação """
    if created:  # Verifica se a reclamação foi criada
        subject = "Nova Notificação Registrada"
        message = f"""
        Olá,

        Uma nova notificação foi registrada no sistema.

        Título: {instance.titulo}
        Descrição: {instance.descricao}
        Usuário: {instance.usuario.email}

        Estamos enviando essa notificação através do aplicativo "Gestão de Relacionamentos".  
        Por favor, tome as providências necessárias.

        Atenciosamente,
        Sistema de Notificações
        """
        destinatario = 'gestores@exemplo.com'
        send_mail(
            subject,
            message,
            'seu_email@example.com',  # Use settings.DEFAULT_FROM_EMAIL
            [destinatario],
            fail_silently=False,
        )

@receiver(pre_save, sender=Reclamacao)
def registrar_historico_status(sender, instance, **kwargs):
    if instance.pk:  # Verifica se a reclamação já existe no banco de dados
        try:
            reclamacao_anterior = Reclamacao.objects.get(pk=instance.pk)
            if reclamacao_anterior.status != instance.status:
                # Cria uma entrada no HistoricoStatus
                HistoricoStatus.objects.create(
                    reclamacao=instance,
                    status=instance.status,
                    observacao=f"Status alterado automaticamente para {instance.status}."
                )
        except Reclamacao.DoesNotExist:
            # Caso não exista, significa que é um novo registro
            pass
