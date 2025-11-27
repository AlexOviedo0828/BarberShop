from flask_app.config.mysqlconnection import connectToMySQL


class Pedido:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data['id']
        self.usuario_id = data['usuario_id']
        self.peluquero_id = data['peluquero_id']
        self.fecha = data['fecha']
        self.total = data['total']
        self.estado = data['estado']
        self.direccion_envio = data['direccion_envio']
        self.estado_despacho = data['estado_despacho']
        self.metodo_pago = data['metodo_pago']

    # ---------------------------------------
    # CREAR PEDIDO
    # ---------------------------------------

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO pedidos
            (usuario_id, peluquero_id, total, estado,
             direccion_envio, estado_despacho, metodo_pago)
            VALUES (%(usuario_id)s, %(peluquero_id)s, %(total)s, %(estado)s,
                    %(direccion_envio)s, %(estado_despacho)s, %(metodo_pago)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # ---------------------------------------
    # OBTENER PEDIDOS POR USUARIO
    # ---------------------------------------

    @classmethod
    def obtener_por_usuario(cls, data):
        query = "SELECT * FROM pedidos WHERE usuario_id = %(usuario_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return [cls(r) for r in results] if results else []

    # ---------------------------------------
    # TOTAL DE PEDIDOS PENDIENTES
    # ---------------------------------------

    @classmethod
    def pendientes(cls):
        query = """
            SELECT COUNT(id) AS total
            FROM pedidos
            WHERE estado = 'pendiente';
        """
        result = connectToMySQL(cls.db).query_db(query)
        return result[0]['total'] if result else 0
    # Pedidos en curso del usuario


    @classmethod
    def en_curso(cls, data):
        query = """
            SELECT COUNT(id) AS total
            FROM pedidos
            WHERE usuario_id = %(usuario_id)s
            AND estado IN ('pendiente', 'pagado');
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]['total'] if result else 0


    # Últimos pedidos del usuario
    @classmethod
    def ultimos(cls, data):
        query = """
            SELECT id, total, estado, fecha
            FROM pedidos
            WHERE usuario_id = %(usuario_id)s
            ORDER BY fecha DESC
            LIMIT 5;
        """
        return connectToMySQL(cls.db).query_db(query, data)
