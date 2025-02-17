from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from .views import reclamacoes_forms
from .views import success_page

# Importações organizadas
from .views import (
    home,
    signup_view,
    dashboard,
    registrar_reclamacao,
    minhas_reclamacoes,
    toggle_contrast,
    UserChangeListView,
    UserCreateView,
    listar_usuarios,
    criar_reclamacao,
)

# Importações das Views da API
from comunicacao.views import (
    ReclamacaoListCreate,
    ReclamacaoDetail,
    CategoriaListCreate,
    HistoricoStatusList,
    ReclamacaoImagemList,
)

# Teste simples de resposta HTTP
def simple_test_view(request):
    return HttpResponse(render_to_string('simple_test.html'))

urlpatterns = [
    # Página inicial
    path('', home, name='home'),

    # Autenticação
    path('login/', LogoutView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),

    # Admin Django
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # Dashboard e Menu
    path('dashboard/', dashboard, name='dashboard'),

    # Encerramento do sistema
    path('encerramento/', TemplateView.as_view(template_name='encerramento.html'), name='encerramento'),

    # Gerenciamento de Usuários
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path('usuarios/add/', UserCreateView.as_view(), name='comunicacao_user_add'),
    path('usuarios/list/', UserChangeListView.as_view(), name='comunicacao_usuario_changelist'),

    # Reclamações
    path('registrar-reclamacao/', registrar_reclamacao, name='registrar_reclamacao'),
    path('reclamacao/nova/', criar_reclamacao, name='nova_reclamacao'),
    path('minhas-reclamacoes/', minhas_reclamacoes, name='minhas_reclamacoes'),
    path('formulario-reclamacao/', reclamacoes_forms, name='reclamacoes_forms'),
    path('formulario-reclamacao/sucesso/', success_page, name='success_page'),

    # Alternar Contraste
    path('toggle-contrast/', toggle_contrast, name='toggle_contrast'),

    # API REST para comunicação com o Android
    path('api/reclamacoes/', ReclamacaoListCreate.as_view(), name='reclamacoes-list'),
    path('api/reclamacoes/<int:pk>/', ReclamacaoDetail.as_view(), name='reclamacao-detail'),
    path('api/categorias/', CategoriaListCreate.as_view(), name='categorias-list'),
    path('api/reclamacoes/<int:reclamacao_id>/historico/', HistoricoStatusList.as_view(), name='historico-status-list'),
    path('api/reclamacoes/<int:reclamacao_id>/imagens/', ReclamacaoImagemList.as_view(), name='reclamacao-imagens-list'),

    # Página de teste simples
    path('simple-test/', simple_test_view, name='simple_test'),
]

# Servir arquivos de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




















