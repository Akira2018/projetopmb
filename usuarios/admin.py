from django.contrib import admin
from usuarios.models import CustomUser

# Define a classe CustomUserAdmin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'telefone')  # Inclua 'telefone' aqui
    search_fields = ('username', 'email', 'first_name', 'last_name', 'telefone')  # Inclua 'telefone' aqui também

# Tenta registrar o modelo CustomUser
try:
    admin.site.register(CustomUser, CustomUserAdmin)
except admin.sites.AlreadyRegistered:
    pass  # Ignora se já estiver registrado





