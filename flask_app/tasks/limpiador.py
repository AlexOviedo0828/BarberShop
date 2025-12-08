from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL

db = "barbershop_db"

def reset_reservas_semanales():
    print("== Reiniciando reservas de barberos ==", datetime.now())

    # Poner reservado = 0 en todos los horarios
    query = "UPDATE horarios SET reservado = 0;"
    connectToMySQL(db).query_db(query)

    print("✔ Todos los horarios han sido liberados (reservado = 0)\n")
