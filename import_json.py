import json
import psycopg2
import os
import urllib.parse

# 🔹 Pegando a URL do banco de dados das variáveis de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ Erro: A variável de ambiente DATABASE_URL não está configurada.")

# 🔹 Ajustando a URL do banco
urllib.parse.uses_netloc.append("postgres")

# 🔹 Conectando ao banco de dados PostgreSQL no Heroku
conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cursor = conn.cursor()

# 🔹 Ler o arquivo JSON sem erros de caracteres especiais
with open("comunicacao_categoria.json", "r", encoding="utf-8", errors="replace") as file:
    dados = json.load(file)

# 🔹 Inserir os dados no banco de dados
for item in dados:
    cursor.execute(
        """
        INSERT INTO comunicacao_categoria (descricao, departamento, email_departamento)
        VALUES (%s, %s, %s)
        """,
        (item["descricao"], item["departamento"], item["email_departamento"])
    )

# 🔹 Salvar alterações e fechar conexão
conn.commit()
cursor.close()
conn.close()

print("✅ Dados importados com sucesso!")
