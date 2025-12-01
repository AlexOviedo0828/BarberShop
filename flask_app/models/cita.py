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
        self.notas = data.get("notas")
        self.duracion_minutos = data.get("duracion_minutos", 30)

    # ===============================================================
    #  Citas de hoy (para dashboard admin)
    # ===============================================================
    @classmethod
    def hoy(cls):
        query = """
            SELECT COUNT(id) AS total
            FROM citas
            WHERE fecha = CURDATE();
        """
        result = connectToMySQL(cls.db).query_db(query)
        return result[0]["total"] if result else 0

    # ===============================================================
    # Obtener TODAS las citas (ADMIN)
    # ===============================================================
    @classmethod
    def obtener_todas_con_info(cls):
        query = """
            SELECT c.*,
                   CONCAT(u.nombre, ' ', u.apellido) AS usuario_nombre,
                   u.imagen AS usuario_imagen,
                   CONCAT(p.nombre, ' ', p.apellido) AS peluquero_nombre,
                   p.imagen AS peluquero_imagen
            FROM citas c
            JOIN usuarios u ON u.id = c.usuario_id
            JOIN peluqueros p ON p.id = c.peluquero_id
            ORDER BY c.fecha DESC, c.hora DESC;
        """
        return connectToMySQL(cls.db).query_db(query)
    # Resto de métodos...
    # ===============================================================

    @classmethod
    def ultimas_usuario(cls, data):
        query = """
            SELECT c.id, c.fecha, c.hora, c.estado,
                   CONCAT(p.nombre, ' ', p.apellido) AS peluquero_nombre
            FROM citas c
            JOIN peluqueros p ON p.id = c.peluquero_id
            WHERE c.usuario_id = %(usuario_id)s
            ORDER BY c.fecha DESC, c.hora DESC;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO citas (usuario_id, peluquero_id, fecha, hora, estado, notas, duracion_minutos)
            VALUES (%(usuario_id)s, %(peluquero_id)s, %(fecha)s, %(hora)s, %(estado)s, %(notas)s, %(duracion_minutos)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def cancelar(cls, data):
        query = """
            UPDATE citas
            SET estado = 'cancelada', notas = %(motivo)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def existe_solapamiento(cls, data):
        query = """
            SELECT *
            FROM citas
            WHERE peluquero_id = %(peluquero_id)s
              AND fecha = %(fecha)s
              AND estado IN ('pendiente','confirmada')
              AND (
                    TIME(%(hora)s) BETWEEN hora AND ADDTIME(hora, SEC_TO_TIME(duracion_minutos * 60))
                 OR hora BETWEEN TIME(%(hora)s)
                           AND ADDTIME(%(hora)s, SEC_TO_TIME(%(duracion_minutos)s * 60))
              );
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return len(result) > 0

    @classmethod
    def pendientes_usuario(cls, data):
        query = """
            SELECT c.*, 
                   CONCAT(p.nombre, ' ', p.apellido) AS peluquero_nombre
            FROM citas c
            JOIN peluqueros p ON p.id = c.peluquero_id
            WHERE c.usuario_id = %(usuario_id)s
              AND c.estado IN ('pendiente', 'confirmada')
            ORDER BY c.fecha ASC, c.hora ASC;
        """
        results = connectToMySQL(cls.db).query_db(query, data)

        citas = []
        if results:
            for row in results:
                cita = cls(row)
                cita.peluquero_nombre = row["peluquero_nombre"]
                citas.append(cita)
        return citas

    @classmethod
    def proxima(cls, data):
        query = """
            SELECT c.*, 
                   CONCAT(p.nombre, ' ', p.apellido) AS peluquero_nombre
            FROM citas c
            JOIN peluqueros p ON p.id = c.peluquero_id
            WHERE c.usuario_id = %(usuario_id)s
              AND c.estado IN ('pendiente', 'confirmada')
              AND CONCAT(c.fecha, ' ', c.hora) > NOW()
            ORDER BY c.fecha ASC, c.hora ASC
            LIMIT 1;
        """
        results = connectToMySQL(cls.db).query_db(query, data)

        if results:
            cita = cls(results[0])
            cita.peluquero_nombre = results[0]["peluquero_nombre"]
            return cita

        return None

    @classmethod
    def ultimas(cls, limite):
        query = """
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
            LIMIT %(limite)s;
        """
        data = {"limite": limite}
        return connectToMySQL(cls.db).query_db(query, data)
