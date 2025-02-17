import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ✅ Defina o caminho das credenciais aqui
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "caminho/completo/para/google-credentials.json"

def get_gmail_service():
    """Autentica e retorna o serviço do Gmail API"""
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        scopes=["https://www.googleapis.com/auth/gmail.send"]
    )
    service = build("gmail", "v1", credentials=credentials)
    return service
