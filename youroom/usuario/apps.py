from django.apps import AppConfig


class UsuarioConfig(AppConfig):
    name = 'usuario'

    def ready(self):
        print("Iniciando el actualizador de vidas y el cancelador de suscripciones")
        from usuario.scheduler import scheduler
        scheduler.restablecer()
        scheduler.cancelar()
