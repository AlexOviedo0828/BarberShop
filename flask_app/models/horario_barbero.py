# flask_app/models/horario_barbero.py
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class HorarioBarbero:
    db_name = "barbershop_db"

    def __init__(self, data):
        self.id = data['id']
        self.barbero_id = data['barbero_id']
        self.dia = data['dia']
        self.hora_inicio = str(data['hora_inicio'])
        self.hora_fin = str(data['hora_fin'])
        self.reservado = data.get('reservado', 0)
        self.descanso_inicio = str(
            data['descanso_inicio']) if data['descanso_inicio'] else None
        self.descanso_fin = str(
            data['descanso_fin']) if data['descanso_fin'] else None
        self.creado_en = data['creado_en']
        # campos extra del join
        self.barbero_nombre = data.get('barbero_nombre', None)

    # Crear
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO horarios_barbero
            (barbero_id, dia, hora_inicio, hora_fin, descanso_inicio, descanso_fin)
            VALUES (%(barbero_id)s, %(dia)s, %(hora_inicio)s, %(hora_fin)s,
                    %(descanso_inicio)s, %(descanso_fin)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Obtener todos con nombre del barbero
    @classmethod
    def get_all_with_barbero(cls):
        query = """
            SELECT h.*,
                   CONCAT(p.nombre, ' ', p.apellido) AS barbero_nombre
            FROM horarios_barbero h
            JOIN peluqueros p ON p.id = h.barbero_id
            ORDER BY p.nombre, h.dia, h.hora_inicio;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        horarios = []
        if results:
            for row in results:
                horarios.append(cls(row))
        return horarios

    # Obtener uno
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM horarios_barbero WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return cls(results[0])
        return None

    # Actualizar
    @classmethod
    def update(cls, data):
        query = """
            UPDATE horarios_barbero
            SET barbero_id = %(barbero_id)s,
                dia = %(dia)s,
                hora_inicio = %(hora_inicio)s,
                hora_fin = %(hora_fin)s,
                descanso_inicio = %(descanso_inicio)s,
                descanso_fin = %(descanso_fin)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Eliminar
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM horarios_barbero WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Validación simple
    @staticmethod
    def validate(form):
        is_valid = True

        if form['hora_inicio'] >= form['hora_fin']:
            flash("La hora de inicio debe ser menor que la hora fin", "horario")
            is_valid = False

        if form.get('descanso_inicio') and form.get('descanso_fin'):
            if form['descanso_inicio'] >= form['descanso_fin']:
                flash("El descanso inicio debe ser menor que descanso fin", "horario")
                is_valid = False

        if not form.get('barbero_id'):
            flash("Debes seleccionar un barbero", "horario")
            is_valid = False

        if not form.get('dia'):
            flash("Debes seleccionar un día", "horario")
            is_valid = False

        return is_valid
