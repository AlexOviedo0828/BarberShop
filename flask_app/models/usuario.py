from flask_app.config.mysqlconnection import connectToMySQL


class Usuario:
    db = "barbershop_db"

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.rol = data['rol']
        self.telefono = data['telefono']
        self.fecha_registro = data['fecha_registro']

    # crear

    @classmethod
    def crear(cls, data):
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password, rol, telefono)
        VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, %(rol)s, %(telefono)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # obtener por email

    @classmethod
    def obtener_por_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s LIMIT 1;"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
# obtener por id

    def obtener_por_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s LIMIT 1;"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
