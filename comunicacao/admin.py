from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usuarios.models import CustomUser  # Certifique-se de usar o caminho correto
from .models import Categoria, Reclamacao, HistoricoStatus, ReclamacaoImagem
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "Gestão de Relacionamentos"
    site_title = "Administração"
    index_title = "Bem-vindo"
    template_name = "admin/base_site.html"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        return urls

    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = ['/static/css/admin_custom.css']  # Caminho para o CSS
        return context

admin_site = CustomAdminSite()
admin_site.register(CustomUser)

@staff_member_required
def custom_view(request):
    return render(request, 'admin/custom_view.html')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'telefone')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'telefone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'telefone')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Adiciona ou remove o usuário do grupo 'Gestores' com base no status de membro da equipe
        if obj.is_staff:
            group, created = Group.objects.get_or_create(name='Gestores')
            obj.groups.add(group)
        else:
            group = Group.objects.filter(name='Gestores').first()
            if group:
                obj.groups.remove(group)

class ReclamacaoImagemInline(admin.TabularInline):
    model = ReclamacaoImagem
    extra = 1

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'departamento')  # Certifique-se de que os campos existem no modelo
    search_fields = ('descricao', 'departamento')  # Também verifique esses campos
    ordering = ('descricao', 'departamento')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'categoria':  # Certifique-se de que 'categoria' é um campo ForeignKey
            kwargs['queryset'] = Categoria.objects.all().order_by('descricao')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_module_permission(self, request):
        # Oculta do menu principal
        return False

@admin.register(Reclamacao)
class ReclamacaoAdmin(admin.ModelAdmin):
    exclude = ['usuario']  # Esconde o campo "Usuário" no formulário
    inlines = [ReclamacaoImagemInline]
    list_display = ('titulo', 'usuario', 'status', 'data_envio')
    list_filter = ('titulo','status', 'categoria')
    search_fields = ('titulo', 'descricao', 'usuario__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusuário vê todas as reclamações
        return qs.filter(usuario=request.user)  # Usuário normal vê apenas suas reclamações

    def save_model(self, request, obj, form, change):
        if not change:  # Se for um novo registro
            obj.usuario = request.user  # Define o usuário logado como o autor
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields.pop('usuario', None)  # Remove o campo 'usuario' para usuários normais
        return form

    def has_module_permission(self, request):
        # Oculta do menu principal
        return False

@admin.register(HistoricoStatus)
class HistoricoStatusAdmin(admin.ModelAdmin):
    list_display = ("reclamacao", "status", "data_alteracao", "get_usuario")
    search_fields = ("reclamacao__titulo", "status")
    list_filter = ("status", "data_alteracao")

    def get_usuario(self, obj):
        return obj.reclamacao.usuario.username  # Substitua "usuario" pelo campo correto no modelo Reclamacao

    get_usuario.short_description = 'Usuário'  # Define a legenda como "Usuário"

    def get_queryset(self, request):
        # Obtém o queryset padrão
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuário vê todas as reclamações
            return qs
        # Usuário normal vê apenas o histórico das reclamações que ele criou
        return qs.filter(reclamacao__usuario=request.user)

    def has_module_permission(self, request):
        # Oculta do menu principal
        return False

