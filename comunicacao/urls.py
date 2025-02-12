from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import TemplateView
from .views import CustomLoginView
###########################################
from comunicacao.views import home, signup  # Importe as funções home e signup do módulo todos.views
from django.contrib.auth.views import LogoutView  # Importe a view de logout padrão do Django
from comunicacao import views  # Importe o views que contém lista_autores
from .views import home, toggle_contrast
from . import views
#################################################
from django.http import HttpResponse  # Import necessário para retornar uma resposta HTTP
from django.template.loader import render_to_string  # Import necessário para carregar o template

from .views import (
    home,
    signup_view,
    dashboard,
    registrar_reclamacao,
    minhas_reclamacoes,
    toggle_contrast,
    index,
    UserChangeListView,
    UserCreateView,
    listar_usuarios,  # Importar a função listar_usuarios
    criar_reclamacao,
)

def simple_test_view(request):
    return HttpResponse(render_to_string('simple_test.html'))

urlpatterns = [
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Inclui URLs de autenticação padrão
    path('dashboard/', views.dashboard, name='dashboard'),

    path('encerramento/', TemplateView.as_view(template_name='encerramento.html'), name='encerramento'),
    # Gerenciamento de usuários
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path('usuarios/add/', UserCreateView.as_view(), name='comunicacao_user_add'),  # Adicionar usuário
    path('usuarios/list/', UserChangeListView.as_view(), name='comunicacao_usuario_changelist'),  # Lista no Admin
    path('simple-test/', simple_test_view, name='simple_test'),
    # Reclamações
    path('registrar-reclamacao/', registrar_reclamacao, name='registrar_reclamacao'),
    path('reclamacao/nova/', criar_reclamacao, name='nova_reclamacao'),
    path('minhas-reclamacoes/', minhas_reclamacoes, name='minhas_reclamacoes'),
    path('formulario-reclamacao/', views.reclamacoes_forms, name='reclamacoes_forms'),
    path('formulario-reclamacao/sucesso/', views.success_page, name='success_page'),
    # Alternar contraste
    path('toggle-contrast/', toggle_contrast, name='toggle_contrast'),
]

# Servir arquivos de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



















