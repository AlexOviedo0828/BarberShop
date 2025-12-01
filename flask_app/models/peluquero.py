from flask_app.config.mysqlconnection import connectToMySQL
import json


class Peluquero:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.especialidad = data['especialidad']
        self.telefono = data['telefono']

        # CONVERTIR DE JSON → DICCIONARIO
        if data['imagen']:
            try:
                self.imagen = json.loads(data['imagen'])
            except:
                self.imagen = None
        else:
            self.imagen = None

        self.servicios_realizados = data['servicios_realizados']
        self.fecha_creacion = data['fecha_creacion']
        self.disponible = data['disponible']

    # ============================
    # TRAER TODOS
    # ============================
    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM peluqueros;"
        results = connectToMySQL(cls.db).query_db(query)
        peluqueros = []
        for p in results:
            peluqueros.append(cls(p))
        return peluqueros

    # ============================
    # INSERTAR
    # ============================
    @classmethod
    def insert(cls, data):
        query = """
            INSERT INTO peluqueros 
            (nombre, apellido, especialidad, telefono, imagen, servicios_realizados, fecha_creacion, disponible)
            VALUES (%(nombre)s, %(apellido)s, %(especialidad)s, %(telefono)s, %(imagen)s, %(servicios_realizados)s, NOW(), 1);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # ============================
    # OBTENER POR ID
    # ============================
    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM peluqueros WHERE id = %(id)s LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0]) if result else None

    # ============================
    # ACTUALIZAR
    # ============================
    @classmethod
    def update(cls, data):
        query = """
            UPDATE peluqueros
            SET nombre=%(nombre)s,
                apellido=%(apellido)s,
                especialidad=%(especialidad)s,
                telefono=%(telefono)s,
                imagen=%(imagen)s,
                servicios_realizados=%(servicios_realizados)s,
                disponible=%(disponible)s
            WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # ============================
    # ELIMINAR
    # ============================
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM peluqueros WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def total(cls):
        query = "SELECT COUNT(*) AS total FROM peluqueros;"
        result = connectToMySQL('barbershop_db').query_db(query)
        return result[0]['total']
