from flask_app.config.mysqlconnection import connectToMySQL


class Usuario:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]
        self.telefono = data["telefono"]
        self.rol = data["rol"]

        self.created_at = data.get("created_at", None)
        self.updated_at = data.get("updated_at", None)

    # OBTENER POR EMAIL

    @classmethod
    def obtener_por_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query, data)

        if not result:
            return False

        return cls(result[0])

    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query, data)

        if not result:
            return False

        return cls(result[0])

    # OBTENER TODOS

    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(row) for row in results]

    # CREAR

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password, rol, telefono)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, %(rol)s, %(telefono)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # ACTUALIZAR

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE usuarios
            SET nombre=%(nombre)s, apellido=%(apellido)s,
                email=%(email)s, telefono=%(telefono)s, rol=%(rol)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # ELIMINAR

    @classmethod
    def eliminar(cls, data):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def total(cls):
        query = "SELECT COUNT(id) AS total FROM usuarios;"
        result = connectToMySQL(cls.db).query_db(query)
        return result[0]["total"] if result else 0

    @classmethod
    def contar_pendientes(cls):
        query = "SELECT COUNT(id) AS total FROM pedidos WHERE estado = 'pendiente';"
        result = connectToMySQL(cls.db).query_db(query)
        return result[0]["total"] if result else 0
