from apscheduler.schedulers.background import BackgroundScheduler
from usuario.views import ShedulerJob


def cancelar():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ShedulerJob.cancelar_suscripcion, 'interval', minutes=1, id="cancelar_suscripcion", replace_existing=True)
    scheduler.start()


def restablecer():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ShedulerJob.restablecer_vidas, 'interval', minutes=1, id="restablecer_vidas", replace_existing=True)
    scheduler.start()


def restablecer_puntos():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ShedulerJob.restablecer_puntos_ranking, 'interval', minutes=1, id="restablecer_puntos_ranking", replace_existing=True)
    scheduler.start()
