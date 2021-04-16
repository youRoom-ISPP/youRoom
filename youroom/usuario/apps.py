from django.apps import AppConfig


class UsuarioConfig(AppConfig):
    name = 'usuario'

    def ready(self):
        print("Iniciando el cancelador de suscripciones")
        from usuario.scheduler import scheduler
        scheduler.cancelar()
