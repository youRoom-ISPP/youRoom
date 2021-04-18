from apscheduler.schedulers.background import BackgroundScheduler
from usuario.views import restablecer_vidas
from usuario.views import cancelar_suscripcion


def cancelar():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cancelar_suscripcion, 'interval', minutes=1, id="cancelar_suscripcion", replace_existing=True)
    scheduler.start()


def restablecer():
    scheduler = BackgroundScheduler()
    scheduler.add_job(restablecer_vidas, 'interval', minutes=1, id="restablecer_vidas", replace_existing=True)
    scheduler.start()
