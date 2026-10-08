from django.apps import AppConfig


class InteroperabilidadeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interoperabilidade'

    def ready(self):
        import interoperabilidade.signals
