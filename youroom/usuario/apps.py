from django.apps import AppConfig


class UsuarioConfig(AppConfig):
    name = 'usuario'

    def ready(self):
        print("Iniciando el actualizador de vidas")
        from usuario.scheduler import scheduler
        scheduler.restablecer()
