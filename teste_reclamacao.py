import os
import django

# Configurar o Django para acessar os modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comunicacao_proj.settings") # 🔹 Substitua "seu_projeto" pelo nome do seu projeto
django.setup()

from comunicacao.models import Reclamacao
from usuarios.models import CustomUser

# Pegue a última reclamação cadastrada
reclamacao = Reclamacao.objects.last()

if reclamacao:
    usuario = reclamacao.usuario  # Obtém o usuário associado à reclamação

    print("\n📌 **DEBUG: DADOS DO USUÁRIO**")
    print(f"Usuário (username): {usuario.username if usuario.username else 'Usuário Anônimo'}")
    print(f"Nome Completo (first_name): {usuario.first_name if usuario.first_name else 'Nome não informado'}")
    print(f"E-mail: {usuario.email if usuario.email else 'E-mail não informado'}")
    print(f"Telefone: {usuario.telefone if usuario.telefone else 'Telefone não informado'}")
    print("🔹 **FIM DO DEBUG**\n")
else:
    print("❌ Nenhuma reclamação encontrada no banco de dados.")

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

