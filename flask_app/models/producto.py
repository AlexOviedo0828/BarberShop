from flask_app.config.mysqlconnection import connectToMySQL


class Producto:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.precio = data['precio']
        self.stock = data['stock']
        self.imagen = data['imagen']
        self.categoria_id = data['categoria_id']
        self.ventas = data['ventas']
        self.fecha_creacion = data['fecha_creacion']
# crear

    @classmethod
    def crear(cls, data):
        query = """
        INSERT INTO productos (nombre, descripcion, precio, stock, imagen, categoria_id)
        VALUES (%(nombre)s, %(descripcion)s, %(precio)s, %(stock)s, %(imagen)s, %(categoria_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)
# obtener

    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM productos;"
        resultado = connectToMySQL(cls.db).query_db(query)
        return [cls(p) for p in resultado]
# obtener por id

    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM productos WHERE id = %(id)s;"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
