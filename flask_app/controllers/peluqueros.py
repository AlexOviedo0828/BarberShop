from flask_app import app
from flask import render_template, request, redirect, flash
from flask_app.models.peluquero import Peluquero


@app.route('/admin/peluqueros')
def listar_peluqueros():
    return "Listado de peluqueros"


@app.route('/admin/peluqueros/nuevo')
def nuevo_peluquero():
    return "Formulario crear peluquero"


@app.route('/admin/peluqueros/crear', methods=['POST'])
def crear_peluquero():
    return "Guardar peluquero"


@app.route('/admin/peluqueros/editar/<int:id>')
def editar_peluquero(id):
    return f"Editar peluquero {id}"


@app.route('/admin/peluqueros/actualizar/<int:id>', methods=['POST'])
def actualizar_peluquero(id):
    return "Actualizar peluquero"


@app.route('/admin/peluqueros/eliminar/<int:id>')
def eliminar_peluquero(id):
    return f"Eliminar peluquero {id}"
