from apscheduler.schedulers.background import BackgroundScheduler
from usuario.views import cancelar_suscripcion


def cancelar():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cancelar_suscripcion, 'interval', minutes=1, id="cancelar_suscripcion", replace_existing=True)
    scheduler.start()
