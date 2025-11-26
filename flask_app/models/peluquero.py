from flask_app.config.mysqlconnection import connectToMySQL


class Peluquero:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.especialidad = data['especialidad']
        self.telefono = data['telefono']
        self.imagen = data['imagen']
        self.servicios_realizados = data['servicios_realizados']
        self.fecha_creacion = data['fecha_creacion']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM peluqueros;"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(r) for r in results] if results else []

    # TOTAL DE PELUQUEROS

    @classmethod
    def total(cls):
        query = "SELECT COUNT(id) AS total FROM peluqueros;"
        result = connectToMySQL(cls.db).query_db(query)
        return result[0]['total'] if result else 0

    # OBTENER PELUQUERO POR ID

    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM peluqueros WHERE id = %(id)s LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0]) if result else None
