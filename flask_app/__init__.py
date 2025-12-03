from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "Alex"

bcrypt = Bcrypt(app)

from apscheduler.schedulers.background import BackgroundScheduler
from flask_app.tasks.limpiador import reset_reservas_semanales

def iniciar_scheduler():
    scheduler = BackgroundScheduler(timezone="America/Bogota")
    scheduler.add_job(
        reset_reservas_semanales,
        trigger="cron",
        day_of_week="sun",
        hour=0,
        minute=0
    )
    scheduler.start()
    print(">>> Scheduler iniciado correctamente.")

# Evita doble ejecución en modo debug
if __name__ != "__main__":
    iniciar_scheduler()