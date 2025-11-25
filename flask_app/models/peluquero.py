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

    # Crear peluquero
    @classmethod
    def crear(cls, data):
        query = """
        INSERT INTO peluqueros (nombre, apellido, especialidad, telefono, imagen)
        VALUES (%(nombre)s, %(apellido)s, %(especialidad)s, %(telefono)s, %(imagen)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # Obtener todos
    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM peluqueros;"
        resultado = connectToMySQL(cls.db).query_db(query)
        return [cls(p) for p in resultado]

    # Obtener por id
    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM peluqueros WHERE id = %(id)s;"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
