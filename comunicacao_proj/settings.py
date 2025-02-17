import os
from pathlib import Path
import django_heroku
import dj_database_url
from urllib.parse import urlparse

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-li1dd3ijq(uutb#ksg*-u++-xqrs8b_h&r3wobp2^v0snk&wha'

# Configuração da conexão com o Docker Engine
#DOCKER_BASE_URL = 'unix://var/run/docker.sock'  # ou 'tcp://127.0.0.1:2375' para conexão remota
DOCKER_BASE_URL = 'TCP://127.0.0.1:2375' ##para conexão remota
DOCKER_API_VERSION = 'auto'  # para detectar automaticamente a versão da API Docker

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
ALLOWED_HOSTS = ['192.168.0.203','127.0.0.1', 'localhost']

ADMIN_URL = 'admin/'  # Defina o URL do painel de administração
LOGIN_URL = '/accounts/login/'
CSRF_COOKIE_SECURE = False  # Defina como True se estiver usando HTTPS
CSRF_USE_SESSIONS = False

CSRF_TRUSTED_ORIGINS = [
    "http://192.168.0.203",
    "http://127.0.0.1",
    "http://localhost",
    "https://projetopmb-1828de3d0b28.herokuapp.com"
]

#CSRF_TRUSTED_ORIGINS = ['https://escolae-255a9c5574fe.herokuapp.com/']

# Define o tempo de expiração da sessão em segundos (por exemplo, 1 hora)
SESSION_COOKIE_AGE = 3600

# Redirecionar após login
# Redirecionamentos após login e logout
LOGIN_REDIRECT_URL = '/dashboard/'  # Substitua '/dashboard/' pela URL desejada
LOGOUT_REDIRECT_URL = '/'  # Substitua '/' pela URL da tela inicial, se necessário

#LOGIN_REDIRECT_URL = '/accounts/profile/'
#LOGIN_REDIRECT_URL = '/'

# settings.py

# Define o template para a página 403
handler403 = 'django.views.defaults.permission_denied'

# Use apenas uma classe CustomUser
AUTH_USER_MODEL = 'usuarios.CustomUser'

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configurar o diretório dos arquivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configurações para envio de e-mail (substitua pelos dados do seu servidor SMTP)
import os

GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, 'google-credentials.json')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'oucaminhavoz2025@gmail.com'
EMAIL_HOST_PASSWORD = 'zdms vplw ajhe pzcg'

# Adicione para ver os logs de erro no terminal
#import logging
#logging.basicConfig(level=logging.DEBUG)

#EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

#DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Configuração de Logging
# Configuração de Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# Configure TEMPLATE_DIR
TEMPLATE_DIR = os.path.join(BASE_DIR, 'comunicacao/templates')

# Configuração dos Templates
# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'comunicacao', 'templates')],  # Caminho para as pastas de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS = [
    # Aplicações padrão do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Bibliotecas de terceiros
    'corsheaders',
    'grappelli',
    # Sua aplicação principal
    'comunicacao',
    'usuarios',
    'bootstrap5',
]

# Configuração opcional para tags de mensagens
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'error',
    messages.SUCCESS: 'success',
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Primeiro
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Certifique-se de que esse middleware está presente
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'comunicacao.middleware.ForeignKeyActivationMiddleware',

]

# Configurações do Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_HEADERS = [
    'Accept',
    'Accept-Language',
    'Content-Language',
    'Content-Type',
    'Authorization',
]

SUIT_CONFIG = {
    'ADMIN_NAME': 'Django administration',
    'MENU': (
        'sites',
        {'label': 'Custom', 'icon': 'icon-cog', 'models': ('auth.user', 'auth.group')},
        {'label': 'Blog', 'icon': 'icon-book', 'models': ('blog.category', 'blog.post')},
    )
}

ROOT_URLCONF = 'comunicacao.urls'

WSGI_APPLICATION = 'comunicacao_proj.wsgi.application'

# Configurações do Banco de Dados

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'Reclamacoes.sqlite3',  # Localização do banco de dados
    }
}

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


# Configuração do banco de dados para produção no Heroku
DATABASE_URL = os.getenv('DATABASE_URL')  # Obtém a URL do banco de dados do Heroku

if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(default=DATABASE_URL, conn_max_age=600)


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# Outras configurações
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = False
USE_TZ = True

import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivos de Mídia (Imagens)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#MAGEM_LIVROS = os.path.join(MEDIA_ROOT, 'Livros', 'Imagembiblioteca.jpg')

SQLITE3_ROOT = os.path.join(BASE_DIR, 'sqlite3')
SQLITE3_URL = "/venv/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

django_heroku.settings(locals())
