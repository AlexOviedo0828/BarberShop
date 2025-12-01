from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.controllers.usuarios import is_admin
from flask_app.models.usuario import Usuario
from flask_app.models.peluquero import Peluquero
from flask_app.models.cita import Cita
from flask_app.models.pedido import Pedido


@app.route('/dashboard/admin')
def dashboard_admin():
    # Validación de sesión
    if 'usuario_id' not in session:
        return redirect('/login')

    # Validación de rol (solo admin)
    if session.get('rol') != 'admin':
        return redirect('/dashboard/usuario')

    # Datos del dashboard
    data = {
        "total_usuarios": Usuario.total(),
        "total_peluqueros": Peluquero.total(),
        "total_citas_hoy": Cita.hoy(),
        "pedidos_pendientes": Pedido.pendientes(),
        "ultimas_citas": Cita.ultimas(5)
    }

    usuario = Usuario.obtener_por_id({"id": session["usuario_id"]})
    nombre = usuario.nombre.capitalize() if usuario else "Admin"

    return render_template("admin.html", nombre=nombre, **data)


@app.route('/admin/usuarios')
def admin_usuarios():
    """
    Muestra la tabla con todos los usuarios para el panel admin.
    """
    if not is_admin():
        return redirect('/login')

    usuarios = Usuario.obtener_todos()
    return render_template("admin_usuarios.html", usuarios=usuarios)


@app.route('/admin/usuarios/nuevo')
def admin_usuario_nuevo():
    """
    Renderiza el formulario para crear un nuevo usuario desde el panel admin.
    """
    if not is_admin():
        return redirect('/login')

    return render_template("admin_usuario_nuevo.html")


@app.route('/admin/usuarios/crear', methods=['POST'])
def admin_usuario_crear():
    """
    Procesa el formulario de creación de usuario.
    """
    if not is_admin():
        return redirect('/login')

    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form.get('telefono')
    rol = request.form.get('rol', 'usuario')
    password = request.form['password']

    Usuario.crear({
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "rol": rol,
        "password": password
    })

    flash("Usuario creado correctamente", "success")
    return redirect('/admin/usuarios')
