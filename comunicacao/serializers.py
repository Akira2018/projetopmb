#serializers.py

from rest_framework import serializers
from .models import Reclamacao, Categoria, HistoricoStatus, ReclamacaoImagem

# Serializer para Reclamações
class ReclamacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reclamacao
        fields = '__all__'  # Inclui todos os campos

# Serializer para Categorias
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# Serializer para Histórico de Status
class HistoricoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoStatus
        fields = '__all__'

# Serializer para Imagens das Reclamações
class ReclamacaoImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReclamacaoImagem
        fields = '__all__'
