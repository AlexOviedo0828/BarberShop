from flask_app.config.mysqlconnection import connectToMySQL


class Cita:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data["id"]
        self.usuario_id = data["usuario_id"]
        self.peluquero_id = data["peluquero_id"]
        self.fecha = data["fecha"]
        self.hora = data["hora"]
        self.estado = data["estado"]
        self.notas = data["notas"]
        self.duracion_minutos = data["duracion_minutos"]

    # ----------------------------------------
    # CANTIDAD DE CITAS HOY
    # ----------------------------------------

    @classmethod
    def hoy(cls):
        query = """
            SELECT COUNT(id) AS total
            FROM citas
            WHERE fecha = CURDATE();
        """
        result = connectToMySQL(cls.db).query_db(query)
        return result[0]['total'] if result else 0

    # ----------------------------------------
    # OBTENER LAS ÚLTIMAS N CITAS
    # ----------------------------------------

    @classmethod
    def ultimas(cls, limite):
        query = f"""
            SELECT c.id,
                   CONCAT(u.nombre, ' ', u.apellido) AS usuario_nombre,
                   CONCAT(p.nombre, ' ', p.apellido) AS peluquero_nombre,
                   c.fecha,
                   c.hora,
                   c.estado
            FROM citas c
            JOIN usuarios u ON u.id = c.usuario_id
            JOIN peluqueros p ON p.id = c.peluquero_id
            ORDER BY c.fecha DESC, c.hora DESC
            LIMIT {limite};
        """
        return connectToMySQL(cls.db).query_db(query)
    # Citas pendientes del usuario


@classmethod
def pendientes_usuario(cls, data):
    query = """
        SELECT COUNT(id) AS total
        FROM citas
        WHERE usuario_id = %(usuario_id)s
        AND estado = 'pendiente';
    """
    result = connectToMySQL(cls.db).query_db(query, data)
    return result[0]['total'] if result else 0


# Próxima cita del usuario
@classmethod
def proxima(cls, data):
    query = """
        SELECT c.id, c.fecha, c.hora,
               CONCAT(p.nombre, ' ', p.apellido) AS peluquero_nombre
        FROM citas c
        JOIN peluqueros p ON p.id = c.peluquero_id
        WHERE c.usuario_id = %(usuario_id)s
        AND c.estado IN ('pendiente','confirmada')
        AND c.fecha >= CURDATE()
        ORDER BY c.fecha ASC, c.hora ASC
        LIMIT 1;
    """
    result = connectToMySQL(cls.db).query_db(query, data)
    return result[0] if result else None


# Últimas citas del usuario
@classmethod
def ultimas_usuario(cls, data):
    query = """
        SELECT c.id, c.fecha, c.hora, c.estado,
               CONCAT(p.nombre, ' ', p.apellido) AS peluquero_nombre
        FROM citas c
        JOIN peluqueros p ON p.id = c.peluquero_id
        WHERE c.usuario_id = %(usuario_id)s
        ORDER BY c.fecha DESC, c.hora DESC
        LIMIT 5;
    """
    return connectToMySQL(cls.db).query_db(query, data)
