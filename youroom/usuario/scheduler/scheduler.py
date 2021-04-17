from apscheduler.schedulers.background import BackgroundScheduler
from usuario.views import restablecer_vidas


def restablecer():
    scheduler = BackgroundScheduler()
    scheduler.add_job(restablecer_vidas, 'interval', minutes=1, id="restablecer_vidas", replace_existing=True)
    scheduler.start()
