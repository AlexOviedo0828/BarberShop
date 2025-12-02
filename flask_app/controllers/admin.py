from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.controllers.usuarios import is_admin
from flask_app.models.usuario import Usuario
from flask_app.models.peluquero import Peluquero
from flask_app.models.cita import Cita
from flask_app.models.pedido import Pedido
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


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

    data={
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "telefono": request.form.get('telefono'),
        "rol": request.form.get('rol', 'usuario'),
        "password": request.form['password']
    }

    data['password'] = bcrypt.generate_password_hash(data['password'])

    Usuario.crear(data)

    flash("Usuario creado correctamente", "success")
    return redirect('/admin/usuarios')

@app.route('/admin/usuarios/editar/<int:id>')
def admin_usuario_editar(id):
    """
    Renderiza el formulario para editar un usuario desde el panel admin.
    """
    if not is_admin():
        return redirect('/login')

    usuario = Usuario.obtener_por_id({"id": id})
    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect('/admin/usuarios')

    return render_template("admin_usuario_editar.html", usuario=usuario)

@app.route('/admin/usuarios/actualizar/<int:id>', methods=['POST'])
def admin_usuario_actualizar(id):
    """
    Procesa el formulario de actualización de usuario.
    """
    if not is_admin():
        return redirect('/login')

    data={
        "id": id,
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "telefono": request.form.get('telefono'),
        "rol": request.form.get('rol', 'usuario')
    }

    Usuario.actualizar(data)

    flash("Usuario actualizado correctamente", "success")
    return redirect('/admin/usuarios')

@app.route('/admin/usuarios/eliminar/<int:id>' , methods=['POST'])
def admin_usuario_eliminar(id):
    """
    Elimina un usuario desde el panel admin.
    """
    if not is_admin():
        return redirect('/login')

    Usuario.eliminar({"id": id})

    flash("Usuario eliminado correctamente", "success")
    return redirect('/admin/usuarios')