from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Simulação de um usuário para o teste
class UsuarioTeste:
    username = "TesteUsuario"
    first_name = "Teste"
    last_name = "Usuário"
    email = "luizisrael2015@gmail.com"
    telefone = "(11) 99999-9999"

usuario = UsuarioTeste()  # Criando um usuário fictício para o teste
destinatario_email = "luizisrael2015@gmail.com"  # Substitua pelo e-mail real do destinatário

remetente_email = settings.DEFAULT_FROM_EMAIL  # Pegando do settings.py

# Criando a mensagem HTML
mensagem_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Teste de E-mail</title>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; }}
        h2 {{ color: #D80032; }}
        p {{ margin: 10px 0; }}
        hr {{ border: 1px solid #D80032; }}
    </style>
</head>
<body>
    <h2>📌 Teste de E-mail</h2>
    <hr>
    <p><strong>📌 Usuário:</strong> {usuario.username}</p>
    <p><strong>👤 Nome Completo:</strong> {usuario.first_name} {usuario.last_name}</p>
    <p><strong>✉️ E-mail:</strong> {usuario.email}</p>
    <p><strong>📞 Telefone:</strong> {usuario.telefone}</p>
    <hr>
    <p>Este é um e-mail de teste.</p>
    <p>Verifique se a formatação está correta.</p>
    <br>
    <p><strong>Atenciosamente,</strong><br>
    📌 Teste de Notificações</p>
</body>
</html>
"""

# Criando a versão de texto puro
mensagem_texto = f"""
📌 Teste de E-mail
------------------------------
📌 Usuário: {usuario.username}
👤 Nome Completo: {usuario.first_name} {usuario.last_name}
✉️ E-mail: {usuario.email}
📞 Telefone: {usuario.telefone}
------------------------------
Este é um e-mail de teste.
Verifique se a formatação está correta.

📌 Teste de Notificações
"""

# Criando lista de destinatários
destinatarios = [destinatario_email, usuario.email]  # Enviando para ambos

print("\n📌 **DEBUG: DADOS DO E-MAIL QUE SERÁ ENVIADO**")
print(f"📨 Destinatários: {destinatarios}")
print(f"📨 Assunto: Teste de E-mail")
print(f"📨 Conteúdo do e-mail em HTML:\n{mensagem_html}")
print("🔹 **FIM DO DEBUG**\n")

# Criando o e-mail
email = EmailMultiAlternatives(
    subject="📌 Teste de E-mail",
    body=mensagem_texto,  # Texto plano como fallback
    from_email=remetente_email,
    to=destinatarios,
)

# Adicionar a versão HTML ao e-mail
email.attach_alternative(mensagem_html, "text/html")

# Enviar o e-mail apenas uma vez para os destinatários corretos
email.send(fail_silently=False)

print(f"✅ E-mail enviado para {', '.join(destinatarios)}")
