from django import forms
from django.contrib.auth.forms import UserChangeForm
from usuarios.models import Usuario  # Certifique-se de importar corretamente
from usuarios.models import CustomUser
from .models import Reclamacao, Categoria, HistoricoStatus, Admin
from django.contrib.auth.models import Group

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario  # Certifique-se de que 'Usuario' é o modelo correto.
        fields = ['nome', 'email', 'telefone', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
        }

# Formulário para editar um usuário existente
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'telefone', 'is_staff']

# Formulário de cadastro de usuário
class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirme sua senha")
    membro_da_equipe = forms.BooleanField(initial=True, required=True, label="Membro da equipe")
    telefone = forms.CharField(
        max_length=20,
        required=True,
        label="Número de Telefone",
        widget=forms.TextInput(attrs={'placeholder': '(XX) XXXXX-XXXX', 'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'telefone', 'password']

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not telefone:
            raise forms.ValidationError("O campo Telefone é obrigatório.")
        if not RegexValidator(regex=r'^\(\d{2}\) \d{5}-\d{4}$').regex.match(telefone):
            raise forms.ValidationError("O número de telefone deve estar no formato (XX) XXXXX-XXXX.")
        return telefone

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error("password2", "As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.membro_da_equipe = self.cleaned_data.get("membro_da_equipe", True)
        if commit:
            user.save()
        return user

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirme sua senha")
    membro_da_equipe = forms.BooleanField(required=False, label="Membro da equipe")
    telefone = forms.CharField(max_length=15, required=True, label="Número de Telefone")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'telefone', 'is_staff']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # Define o valor de `is_staff` com base no campo "Membro da Equipe"
        if self.cleaned_data.get("membro_da_equipe", False):
            user.is_staff = True  # Define como 1 para permitir o acesso
        else:
            user.is_staff = False  # Define como 0 caso não seja membro da equipe

        if commit:
            user.save()

            # Adicionar o usuário ao grupo "Gestores"
            group, created = Group.objects.get_or_create(name="Gestores")
            user.groups.add(group)

        return user
class ReclamacaoForm(forms.ModelForm):

    class Meta:
        model = Reclamacao
        fields = ['nome_completo', 'email', 'telefone', 'titulo', 'descricao', 'categoria', 'status', 'imagem']  # Inclui os novos campos
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título',
                'required': 'required',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva aqui',
                'required': 'required',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
                'rows': 2,
                'required': 'required',
                'style': 'width: 100%; font-size: 0.9rem;',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'rows': 2,
                'required': 'required',
                'style': 'width: 100%; font-size: 0.9rem;',
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

        # ✅ Novos campos adicionados (Apenas leitura)

    nome_completo = forms.CharField(
        label="Nome Completo", required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    email = forms.EmailField(
        label="E-mail", required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    telefone = forms.CharField(
        label="Telefone", required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  # Recebe o usuário autenticado
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = 'Fase Inicial'  # Define o valor inicial no formulário

        self.fields['categoria'].queryset = Categoria.objects.order_by('descricao')

        # ✅ Preenche os campos Nome, E-mail e Telefone automaticamente
        if usuario:
            self.fields['nome_completo'].initial = f"{usuario.first_name} {usuario.last_name}".strip()
            self.fields['email'].initial = usuario.email
            self.fields['telefone'].initial = getattr(usuario, 'telefone', '')

    # Validações mantidas
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if not titulo:
            raise forms.ValidationError("O campo Título é obrigatório.")
        return titulo

    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao')
        if not descricao:
            raise forms.ValidationError("O campo Descrição é obrigatório.")
        return descricao

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria:
            raise forms.ValidationError("O campo Categoria é obrigatório.")
        return categoria

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if not status:
            raise forms.ValidationError("O campo Status é obrigatório.")
        return status

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')
        return imagem

# Formulário de cadastro de administrador
class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['usuario', 'email', 'senha']  # Incluído o campo 'senha'
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do administrador'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),  # Ajustado
        }

# Formulário de categoria
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['departamento', 'descricao']
        widgets = {
            'departamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da categoria'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da categoria'}),
        }

# Formulário de histórico de status
class HistoricoStatusForm(forms.ModelForm):
    class Meta:
        model = HistoricoStatus
        fields = ['reclamacao', 'status', 'observacao']
        widgets = {
            'reclamacao': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Novo status'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações sobre a mudança de status'}),
        }
