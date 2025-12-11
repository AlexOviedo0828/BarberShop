from flask_app.config.mysqlconnection import connectToMySQL


class Pedido:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data["id"]
        self.usuario_id = data["usuario_id"]
        self.total = data["total"]
        self.estado = data["estado"]
        self.fecha = data["fecha"]
        self.direccion_envio = data.get("direccion_envio")
        self.metodo_pago = data.get("metodo_pago")

    # OBTENER TODOS

    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM pedidos ORDER BY fecha DESC;"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(p) for p in results] if results else []

    # OBTENER POR ID

    @classmethod
    def obtener_por_id(cls, data):
        query = """
        SELECT pedidos.*, usuarios.nombre AS cliente_nombre
        FROM pedidos
        LEFT JOIN usuarios ON usuarios.id = pedidos.usuario_id
        WHERE pedidos.id = %(id)s;
        """
        resultado = connectToMySQL('barbershop_db').query_db(query, data)

        if resultado:
            pedido = cls(resultado[0])
            pedido.cliente_nombre = resultado[0]["cliente_nombre"]
            return pedido

            return None

    # CREAR PEDIDO

    @classmethod
    def crear(cls, data):
        query = """
        INSERT INTO pedidos (usuario_id, total, estado, fecha, direccion_envio, metodo_pago)
        VALUES (%(usuario_id)s, %(total)s, %(estado)s, NOW(), %(direccion_envio)s, %(metodo_pago)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # ACTUALIZAR

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE pedidos
            SET total=%(total)s,
                estado=%(estado)s,
                direccion_envio=%(direccion_envio)s,
                metodo_pago=%(metodo_pago)s
            WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # ELIMINAR

    @classmethod
    def eliminar(cls, data):
        query = "DELETE FROM pedidos WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # PEDIDOS EN CURSO (para usuario)

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

    # LISTA DE PENDIENTES

    @classmethod
    def obtener_pendientes(cls):
        query = """
            SELECT * FROM pedidos
            WHERE estado = 'pendiente'
            ORDER BY fecha DESC;
        """
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(r) for r in results] if results else []

    # CANTIDAD DE PENDIENTES (para dashboard admin)

    @classmethod
    def pendientes(cls):
        query = "SELECT COUNT(id) AS total FROM pedidos WHERE estado='pendiente';"
        result = connectToMySQL(cls.db).query_db(query)
        return result[0]["total"] if result else 0

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
    def obtener_todos_con_usuario(cls):
        query = """
        SELECT p.*, CONCAT(u.nombre, ' ', u.apellido) AS cliente
        FROM pedidos p
        JOIN usuarios u ON u.id = p.usuario_id
        ORDER BY p.id DESC;
    """
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def obtener_con_usuario_por_id(cls, data):
        query = """
        SELECT p.*, CONCAT(u.nombre, ' ', u.apellido) AS cliente
        FROM pedidos p
        JOIN usuarios u ON u.id = p.usuario_id
        WHERE p.id = %(id)s;
        """
        resultado = connectToMySQL(cls.db).query_db(query, data)
        return resultado[0] if resultado else None

    @classmethod
    def cambiar_estado(cls, data):
        query = "UPDATE pedidos SET estado = %(estado)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def actualizar_estado(cls, data):
        query = """
        UPDATE pedidos 
        SET estado = %(estado)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)
