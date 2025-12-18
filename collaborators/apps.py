from django.apps import AppConfig


class CollaboratorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collaborators'

    def ready(self):
        import collaborators.signals