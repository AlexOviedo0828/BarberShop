from flask_app.config.mysqlconnection import connectToMySQL


class Pedido:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data["id"]
        self.usuario_id = data["usuario_id"]
        self.total = data["total"]
        self.estado = data["estado"]
        self.fecha = data["fecha"]
        self.direccion = data.get("direccion")
        self.metodo_pago = data.get("metodo_pago")

    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM pedidos ORDER BY fecha DESC;"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(p) for p in results] if results else []

    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM pedidos WHERE id = %(id)s LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO pedidos (usuario_id, total, estado, fecha, direccion, metodo_pago)
            VALUES (%(usuario_id)s, %(total)s, %(estado)s, NOW(), %(direccion)s, %(metodo_pago)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE pedidos
            SET total = %(total)s,
                estado = %(estado)s,
                direccion = %(direccion)s,
                metodo_pago = %(metodo_pago)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def eliminar(cls, data):
        query = "DELETE FROM pedidos WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def en_curso(cls, data):
        query = """
            SELECT * FROM pedidos
            WHERE usuario_id = %(usuario_id)s
            AND estado = 'en curso'
            ORDER BY fecha DESC;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return [cls(r) for r in results] if results else []

    @classmethod
    def ultimos(cls, data):
        query = """
            SELECT * FROM pedidos
            WHERE usuario_id = %(usuario_id)s
            ORDER BY fecha DESC
            LIMIT 5;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return [cls(r) for r in results] if results else []

    @classmethod
    def pendientes(cls):
        query = """
            SELECT * FROM pedidos
            WHERE estado = 'pendiente'
            ORDER BY fecha DESC;
        """
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(r) for r in results] if results else []
