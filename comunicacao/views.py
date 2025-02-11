from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from usuarios.models import Usuario
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.models import CustomUser  # Import correto
from .models import Reclamacao, Categoria, HistoricoStatus, ReclamacaoImagem
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView
from django.template import RequestContext
from .forms import ReclamacaoForm

from .forms import (
    ReclamacaoForm,
    UserSignupForm,
    UsuarioForm,
    CategoriaForm,
    HistoricoStatusForm,
    CustomUserCreationForm,
    UserSignupForm
)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True  # Redireciona usuários autenticados

def custom_view(request):
    return render(request, 'admin/custom_view.html', context=RequestContext(request))

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def criar_reclamacao(request):
    if request.method == "POST":
        form = ReclamacaoForm(request.POST, request.FILES)
        if form.is_valid():
            reclamacao = form.save()
            # Salvar a imagem enviada
            if 'imagem' in request.FILES:
                ReclamacaoImagem.objects.create(
                    reclamacao=reclamacao,
                    imagem=request.FILES['imagem']
                )
            return redirect('reclamacoes_list')  # Substitua pelo nome da sua URL de redirecionamento
    else:
        form = ReclamacaoForm()
    return render(request, 'gestao/reclamacao_form.html', {'form': form})

def logout_view(request):
    messages.success(request, "Você saiu do aplicativo com sucesso.")
    return LogoutView.as_view()(request)

def csrf_failure(request, reason=""):
    return HttpResponseForbidden("Erro de CSRF: A verificação falhou.")

@csrf_protect
def minha_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')

        # Faça o processamento necessário
        if username and email:
            messages.success(request, 'Formulário enviado com sucesso!')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')

    return render(request, 'gestao/signup.html'), {'usar_vlibras': True}

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Verificar se o usuário já existe
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Usuário já está cadastrado.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Este e-mail já foi registrado.')
            else:
                form.save()
                messages.success(request, f'Usuário {username} cadastrado com sucesso!')
                return redirect('login')  # Redireciona para a página de login
        else:
            messages.error(request, 'Erro ao cadastrar o usuário. Verifique os dados.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

# Função listar_usuarios
def listar_usuarios(request):
    usuarios = CustomUser.objects.all()  # Use o modelo CustomUser para buscar os dados
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário registrado com sucesso! Faça login para continuar.")
            return redirect("login")  # Redireciona para a página de login
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# View de dashboard

@login_required
def dashboard(request):
    try:
        group_add_url = reverse('admin:auth_group_add')
    except NoReverseMatch:
        group_add_url = None

    context = {
        "is_gestor": request.user.groups.filter(name="Gestores").exists(),
        "group_add_url": group_add_url
    }

    return render(request, 'gestao/dashboard.html', context)

# Página inicial após o login
@login_required
def index(request):
    return render(request, 'admin/base_site.html')

# Página inicial do sistema
def home(request):
    return render(request, 'gestao/home.html')

# View para registrar reclamação
def registrar_reclamacao(request):
    if request.method == 'POST':
        form = ReclamacaoForm(request.POST)
        if form.is_valid():
            reclamacao = form.save(commit=False)
            reclamacao.usuario = request.user
            reclamacao.save()
            messages.success(request, "Notificação registrada com sucesso!")
            return redirect('minhas_reclamacoes')
    else:
        form = ReclamacaoForm()
    return render(request, 'gestao/registrar_reclamacao.html', {'form': form})

@login_required
def reclamacoes_forms(request):
    if request.method == 'POST':
        form = ReclamacaoForm(request.POST, request.FILES)
        if form.is_valid():
            reclamacao = form.save(commit=False)  # Não salva no banco ainda
            reclamacao.usuario = request.user  # Atribui o usuário autenticado
            reclamacao.save()  # Agora salva no banco
            return redirect('success_page')  # Substitua aqui
    else:
        form = ReclamacaoForm()

    return render(request, 'gestao/reclamacoes_forms.html', {'form': form})

# View para listar as reclamações do usuário logado
@login_required
def minhas_reclamacoes(request):
    reclamacoes = Reclamacao.objects.filter(usuario=request.user)
    return render(request, 'gestao/minhas_reclamacoes.html', {'reclamacoes': reclamacoes})

def success_page(request):
    return render(request, 'gestao/success_page.html')

def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')  # Substitua pela URL desejada
    return redirect('/login/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        # Renderizar o formulário de login
        return render(request, 'registration/login.html', {'form': form})

# Alternar contraste do site
def toggle_contrast(request):
    if 'contrast' in request.session:
        del request.session['contrast']
    else:
        request.session['contrast'] = True
    return redirect(request.META.get('HTTP_REFERER', '/'))

# View para listar os usuários do sistema
class UserChangeListView(ListView):
    model = CustomUser
    template_name = "usuarios/user_list.html"
    context_object_name = "usuarios"

# View para criar usuários do sistema
class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserSignupForm
    template_name = 'usuarios/user_form.html'
    success_url = reverse_lazy('gestao_user_changelist')
