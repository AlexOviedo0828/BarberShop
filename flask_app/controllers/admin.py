# controllers/admin.py

from flask import render_template, session, redirect
from flask_app import app

from flask_app.models.usuario import Usuario
from flask_app.models.peluquero import Peluquero
from flask_app.models.cita import Cita
from flask_app.models.pedido import Pedido


@app.route('/dashboard/admin')
def dashboard_admin():

    if 'usuario_id' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return redirect('/dashboard/usuario')

    data = {
        "total_usuarios": Usuario.total(),
        "total_peluqueros": Peluquero.total(),
        "total_citas_hoy": Cita.hoy(),
        "pedidos_pendientes": Pedido.pendientes(),
        "ultimas_citas": Cita.ultimas(5)
    }
    usuario=Usuario.obtener_por_id({"id": session["usuario_id"]})
    print(f'\n\nUSUARIO ADMIN: {usuario}\n\n')
    nombre=usuario.nombre.capitalize()
    return render_template("admin.html", **data, nombre=nombre)

# ADMIN - LISTA DE USUARIOS


@app.route('/admin/usuarios')
def admin_usuarios():

    if 'usuario_id' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return redirect('/dashboard/usuario')

    usuarios = Usuario.obtener_todos()

    return render_template("admin_usuarios.html", usuarios=usuarios)
