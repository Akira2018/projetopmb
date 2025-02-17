from django.apps import AppConfig
from django.db import models

class ComunicacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comunicacao'

    def ready(self):
        from . import signals  # Importe seus signals aqui

        # Certifique-se de que os modelos estão carregados
        from .models import (
            Categoria, Reclamacao, HistoricoStatus
        )


