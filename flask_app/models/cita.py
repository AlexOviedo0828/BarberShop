from flask_app.config.mysqlconnection import connectToMySQL


class Cita:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data['id']
        self.usuario_id = data['usuario_id']
        self.peluquero_id = data['peluquero_id']
        self.fecha = data['fecha']
        self.hora = data['hora']
        self.estado = data['estado']
        self.notas = data['notas']
        self.duracion_minutos = data['duracion_minutos']

    @classmethod
    def crear(cls, data):
        query = """
        INSERT INTO citas (usuario_id, peluquero_id, fecha, hora, notas)
        VALUES (%(usuario_id)s, %(peluquero_id)s, %(fecha)s, %(hora)s, %(notas)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def obtener_por_usuario(cls, data):
        query = "SELECT * FROM citas WHERE usuario_id = %(usuario_id)s;"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        return [cls(c) for c in resultado]
