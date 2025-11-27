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
        self.disponible = data['disponible']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM peluqueros;"
        results = connectToMySQL(cls.db).query_db(query)
        peluqueros = []
        for peluquero in results:
            peluqueros.append(cls(peluquero))
            print(f'\n\nPELUQUERO: {peluquero}\n\n')
        return peluqueros

    # TOTAL DE PELUQUEROS

    @classmethod
    def total(cls):
        query = "SELECT COUNT(id) AS total FROM peluqueros WHERE disponible=1;"
        result = connectToMySQL(cls.db).query_db(query)
        return result[0]['total'] if result else 0

    # OBTENER PELUQUERO POR ID

    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM peluqueros WHERE id = %(id)s LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def insert(cls, data):
        query = """
            INSERT INTO peluqueros (nombre, apellido, especialidad, telefono, imagen, servicios_realizados, fecha_creacion, disponible)
            VALUES (%(nombre)s, %(apellido)s, %(especialidad)s, %(telefono)s, %(imagen)s, %(servicios_realizados)s, NOW(), 1);
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = """
            UPDATE peluqueros
            SET nombre = %(nombre)s,
                apellido = %(apellido)s,
                especialidad = %(especialidad)s,
                telefono = %(telefono)s,
                imagen = %(imagen)s,
                servicios_realizados = %(servicios_realizados)s,
                disponible = %(disponible)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM peluqueros WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)