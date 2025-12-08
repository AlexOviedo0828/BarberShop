from flask_app.config.mysqlconnection import connectToMySQL


class Categoria:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']

    @classmethod
    def crear(cls, data):
        query = "INSERT INTO categorias (nombre) VALUES (%(nombre)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def obtener_todas(cls):
        query = "SELECT * FROM categorias;"
        resultado = connectToMySQL(cls.db).query_db(query)
        return [cls(cat) for cat in resultado]
