from flask_app import app
from flask import render_template, request, redirect
from flask_app.models.cita import Cita


@app.route('/citas')
def mis_citas():
    return "Página de mis citas"


@app.route('/citas/nueva')
def nueva_cita():
    return "Formulario para agendar cita"


@app.route('/citas/crear', methods=['POST'])
def crear_cita():
    return "Crear cita"


@app.route('/citas/cancelar/<int:id>')
def cancelar_cita(id):
    return f"Cancelar cita {id}"
