import os
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from django.core.mail import send_mail, BadHeaderError

# Caminho para o arquivo de credenciais JSON
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'google-credentials.json')

# Carregar as credenciais da conta de serviço
def get_gmail_service():
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/gmail.send']
    )
    service = build('gmail', 'v1', credentials=credentials)
    return service

# Enviar o e-mail
def send_email(to, subject, message_text):
    """Função para enviar e-mail via API do Gmail"""
    try:
        service = get_gmail_service()
        message = create_message('reclamacoes@reclamacoes-444912.iam.gserviceaccount.com', to, subject, message_text)
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        print(f"E-mail enviado para {to} com o ID: {sent_message['id']}")
        return sent_message
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return None

# Criar o e-mail no formato MIME
def create_message(sender, to, subject, message_text):
    """Função para criar o e-mail MIME"""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}
