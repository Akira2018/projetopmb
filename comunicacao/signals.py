from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from comunicacao.models import Reclamacao, Categoria
import os

@receiver(post_save, sender=Reclamacao)
def enviar_email_reclamacao(sender, instance, created, **kwargs):
    """ Enviar e-mail automaticamente após registrar uma nova comunicação """
    if created:  # Verifica se a reclamação foi criada

        usuario = instance.usuario
        categoria = instance.categoria

        try:
            categoria_db = Categoria.objects.get(id=categoria.id)
            destinatario_email = categoria_db.email_departamento.strip() if categoria_db.email_departamento else None
        except Categoria.DoesNotExist:
            print("❌ ERRO: Categoria não encontrada no banco de dados. E-mail não será enviado.")
            return

        if not destinatario_email:
            print("❌ ERRO: A categoria não possui um e-mail de departamento cadastrado. E-mail não será enviado.")
            return

        remetente_email = settings.DEFAULT_FROM_EMAIL

        usuario_nome = usuario.username if usuario.username else "Usuário Anônimo"
        usuario_nome_completo = f"{usuario.first_name} {usuario.last_name}".strip() or "[NOME NÃO INFORMADO]"
        usuario_email = usuario.email if usuario.email else "[E-MAIL NÃO INFORMADO]"
        usuario_telefone = getattr(usuario, 'telefone', "[TELEFONE NÃO INFORMADO]")

        mensagem_html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Nova Reclamação</title>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; margin: 0; padding: 0; }}
                h2 {{ color: #D80032; }}
                p {{ margin: 10px 0; }}
                hr {{ border: 1px solid #D80032; }}
                .container {{ width: 100%; max-width: 600px; margin: auto; padding: 20px; }}
                .content {{ background: #f9f9f9; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h2>📌 <strong>Nova Comunicação Registrada</strong></h2>
                    <hr>
                    <p><strong>📌 Usuário:</strong> {usuario_nome}</p>
                    <p><strong>👤 Nome Completo:</strong> {usuario_nome_completo}</p>
                    <p><strong>✉️ E-mail:</strong> {usuario_email}</p>
                    <p><strong>📞 Telefone:</strong> {usuario_telefone}</p>
                    <p><strong>📌 Título:</strong> {instance.titulo}</p>
                    <p><strong>📄 Descrição:</strong> {instance.descricao}</p>
                    <p><strong>📌 Categoria:</strong> {categoria_db.descricao}</p>
                    <hr>
                    <p>Estamos enviando essa notificação através do aplicativo <strong>Gestão de Relacionamentos</strong>.</p>
                    <p><strong>Por favor, tome as providências necessárias.</strong></p>
                    <br>
                    <p><strong>Atenciosamente,</strong><br>
                    📌 Sistema de Notificações</p>
                    <p><strong>⚠ Atenção:</strong> A resposta desta comunicação deve ser enviada para o e-mail do usuário: <a href="mailto:{usuario_email}">{usuario_email}</a></p>
                </div>
            </div>
        </body>
        </html>
        """

        # Garantindo que apenas um e-mail seja enviado com cópia para o usuário
        destinatario_principal = [usuario_email] if usuario.email else []  # Usuário recebe o e-mail
        copia_usuario = [destinatario_email]  # O destinatário será colocado em cópia

        print(f"🔹 Enviando e-mail para: {destinatario_principal}, com cópia para: {copia_usuario}")

        # Criando e-mail
        email = EmailMultiAlternatives(
            subject="📌 Registro de Comunicação",
            from_email=remetente_email,
            to=destinatario_principal,  # Apenas um destinatário principal
            cc=copia_usuario,  # Usuário recebe uma cópia do e-mail
            reply_to=[usuario_email]  # Define o usuário como remetente de resposta
        )

        # Anexando a versão HTML
        email.attach_alternative(mensagem_html, "text/html")

        # 🔹 Se houver uma imagem anexada, adicionamos ao e-mail
        if instance.imagem:
            imagem_path = instance.imagem.path
            if os.path.exists(imagem_path):
                email.attach_file(imagem_path)

        # Enviar o e-mail
        email.send(fail_silently=False)

        print(f"✅ E-mail enviado corretamente para: {destinatario_email}, com cópia para: {usuario_email}")
