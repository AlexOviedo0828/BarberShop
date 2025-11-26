from flask_app import app
from flask import render_template, request, redirect
from flask_app.models.producto import Producto


@app.route('/admin/productos')
def listar_productos():
    return "Listado de productos"


@app.route('/admin/productos/nuevo')
def nuevo_producto():
    return "Formulario crear producto"


@app.route('/admin/productos/crear', methods=['POST'])
def crear_producto():
    return "Guardar producto"


@app.route('/admin/productos/editar/<int:id>')
def editar_producto(id):
    return f"Editar producto {id}"


@app.route('/admin/productos/actualizar/<int:id>', methods=['POST'])
def actualizar_producto(id):
    return "Actualizar producto"


@app.route('/admin/productos/eliminar/<int:id>')
def eliminar_producto(id):
    return f"Eliminar producto {id}"
