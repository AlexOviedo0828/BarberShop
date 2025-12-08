from flask_app.config.mysqlconnection import connectToMySQL


class DetallePedido:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data['id']
        self.pedido_id = data['pedido_id']
        self.producto_id = data['producto_id']
        self.cantidad = data['cantidad']
        self.precio = data['precio']

    @classmethod
    def crear(cls, data):
        query = """
        INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio)
        VALUES (%(pedido_id)s, %(producto_id)s, %(cantidad)s, %(precio)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def obtener_por_pedido(cls, data):
        query = "SELECT * FROM detalles_pedido WHERE pedido_id = %(pedido_id)s;"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        return [cls(det) for det in resultado]

    @classmethod
    def obtener_detalles_completos(cls, data):
        query = """
        SELECT dp.id, dp.cantidad, dp.precio,
               p.nombre AS producto_nombre,
               p.imagen AS producto_imagen
        FROM detalles_pedido dp
        JOIN productos p ON p.id = dp.producto_id
        WHERE dp.pedido_id = %(pedido_id)s;
    """

        resultado = connectToMySQL(cls.db).query_db(query, data)

        detalles = []
        if resultado:
            for row in resultado:
                item = cls(row)
                item.producto_nombre = row["producto_nombre"]
                item.producto_imagen = row["producto_imagen"]
                detalles.append(item)
        return detalles
