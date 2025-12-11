from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.controllers.usuarios import is_admin
from flask_app.models.usuario import Usuario
from flask_app.models.peluquero import Peluquero
from flask_app.models.cita import Cita
from flask_app.models.pedido import Pedido
from flask_app.models.detalle_pedido import DetallePedido
from flask_app.models.producto import Producto
from flask_bcrypt import Bcrypt
from flask import jsonify
bcrypt = Bcrypt(app)


# DASHBOARD ADMIN

@app.route('/dashboard/admin')
def dashboard_admin():

    if 'usuario_id' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return redirect('/dashboard/usuario')

    data = {
        "total_usuarios": Usuario.total(),
        "total_peluqueros": Peluquero.total(),
        "peluqueros_activos": Peluquero.total_activos(),
        "total_citas_hoy": Cita.hoy(),
        "pedidos_pendientes": Pedido.pendientes(),
        "ultimas_citas": Cita.ultimas_admin(5)
    }

    usuario = Usuario.obtener_por_id({"id": session["usuario_id"]})

    return render_template("admin.html", nombre=usuario.nombre.capitalize(), **data)


# CRUD ADMIN USUARIOS

@app.route('/admin/usuarios')
def admin_usuarios():
    if not is_admin():
        return redirect('/login')

    usuarios = Usuario.obtener_todos()
    return render_template("admin_usuarios.html", usuarios=usuarios)


@app.route('/admin/usuarios/nuevo')
def admin_usuario_nuevo():
    if not is_admin():
        return redirect('/login')

    return render_template("admin_usuario_nuevo.html")


@app.route('/admin/usuarios/crear', methods=['POST'])
def admin_usuario_crear():
    if not is_admin():
        return redirect('/login')

    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "telefono": request.form.get('telefono'),
        "rol": request.form.get('rol', 'usuario'),
        "password": bcrypt.generate_password_hash(request.form['password'])
    }

    Usuario.crear(data)
    flash("Usuario creado correctamente", "success")
    return redirect('/admin/usuarios')


@app.route('/admin/usuarios/editar/<int:id>')
def admin_usuario_editar(id):
    if not is_admin():
        return redirect('/login')

    usuario = Usuario.obtener_por_id({"id": id})

    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect('/admin/usuarios')

    return render_template("admin_usuario_editar.html", usuario=usuario)


@app.route('/admin/usuarios/actualizar/<int:id>', methods=['POST'])
def admin_usuario_actualizar(id):
    if not is_admin():
        return redirect('/login')

    data = {
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


@app.route('/admin/usuarios/eliminar/<int:id>', methods=['POST'])
def admin_usuario_eliminar(id):
    if not is_admin():
        return redirect('/login')

    Usuario.eliminar({"id": id})
    flash("Usuario eliminado correctamente", "success")
    return redirect('/admin/usuarios')

# ADMIN – LISTA DE PEDIDOS


@app.route('/admin/pedidos')
def admin_pedidos():
    if not is_admin():
        return redirect('/login')

    pedidos = Pedido.obtener_todos_con_usuario()

    return render_template("admin_pedidos.html", pedidos=pedidos)

# detalle pedidos desde el admin


@app.route('/admin/pedidos/detalle/<int:id>')
def admin_pedido_detalle(id):
    if not is_admin():
        return redirect('/login')

    pedido = Pedido.obtener_por_id({"id": id})

    detalles = DetallePedido.obtener_por_pedido({"pedido_id": id})

    detalles_completos = []
    for d in detalles:
        producto = Producto.obtener_por_id({"id": d.producto_id})
        detalles_completos.append({
            "producto_nombre": producto.nombre if producto else "Producto eliminado",
            "cantidad": d.cantidad,
            "precio": d.precio,
            "subtotal": d.cantidad * d.precio,
            "imagen": producto.imagen if producto else "no-image.png"
        })

    return render_template(
        "admin_pedido_detalle.html",
        pedido=pedido,
        detalles=detalles_completos
    )
    # --- ACTUALIZAR ESTADO DEL PEDIDO ---


@app.post("/admin/pedidos/estado/<int:id>")
def admin_cambiar_estado(id):
    if not is_admin():
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json()
    nuevo_estado = data.get("estado")

    if not nuevo_estado:
        return jsonify({"error": "Estado inválido"}), 400

    Pedido.cambiar_estado({
        "id": id,
        "estado": nuevo_estado
    })

    return jsonify({"mensaje": "Estado actualizado correctamente", "estado": nuevo_estado})
