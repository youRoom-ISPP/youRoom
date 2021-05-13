from django.apps import AppConfig


class UsuarioConfig(AppConfig):
    name = 'usuario'

    def ready(self):
        print("Jobs ejecutados")
        from usuario.scheduler import scheduler
        scheduler.restablecer()
        scheduler.restablecer_puntos()
        scheduler.cancelar()
