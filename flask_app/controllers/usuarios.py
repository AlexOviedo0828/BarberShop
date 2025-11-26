from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt

from flask_app.models.usuario import Usuario
from flask_app.models.cita import Cita
from flask_app.models.pedido import Pedido

bcrypt = Bcrypt(app)


# MIDDLEWARE: SOLO ADMIN
def is_admin():
    return "usuario_id" in session and session.get("rol") == "admin"


# LOGIN


@app.route('/')
@app.route('/login')
def login_form():
    return render_template('login.html')


@app.route('/login/procesar', methods=['POST'])
def login_procesar():

    email = request.form['email']
    password = request.form['password']

    # Validaciones
    if len(email) == 0 or len(password) == 0:
        flash("Todos los campos son obligatorios", "error")
        return redirect('/login')

    usuario = Usuario.obtener_por_email({"email": email})

    if not usuario:
        flash("El usuario no existe", "error")
        return redirect('/login')

    if not bcrypt.check_password_hash(usuario.password, password):
        flash("Contraseña incorrecta", "error")
        return redirect('/login')

    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    session['rol'] = usuario.rol

    if usuario.rol == "admin":
        return redirect('/dashboard/admin')

    return redirect('/dashboard/usuario')

# REGISTRO


@app.route('/registro')
def registro_form():
    return render_template('registro.html')


@app.route('/registro/procesar', methods=['POST'])
def registro_procesar():

    nombre = request.form.get("nombre", "")
    apellido = request.form.get("apellido", "")
    email = request.form.get("email", "")
    telefono = request.form.get("telefono", "")
    password = request.form.get("password", "")
    password2 = request.form.get("password2", "")

    if len(nombre) < 2:
        flash("El nombre es muy corto", "error")
        return redirect('/registro')

    if len(apellido) < 2:
        flash("El apellido es muy corto", "error")
        return redirect('/registro')

    if len(email) < 5:
        flash("Correo inválido", "error")
        return redirect('/registro')

    if password != password2:
        flash("Las contraseñas no coinciden", "error")
        return redirect('/registro')

    if len(password) < 6:
        flash("La contraseña debe tener mínimo 6 caracteres", "error")
        return redirect('/registro')

    if Usuario.obtener_por_email({"email": email}):
        flash("Este correo ya está registrado", "error")
        return redirect('/registro')

    pw_hash = bcrypt.generate_password_hash(password)

    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "telefono": telefono,
        "password": pw_hash,
        "rol": "usuario"
    }

    Usuario.crear(data)

    flash("Registro exitoso. Inicia sesión.", "success")
    return redirect('/login')


# DASHBOARD USUARIO


@app.route("/dashboard/usuario")
def dashboard_usuario():

    if "usuario_id" not in session:
        return redirect("/login")

    usuario = Usuario.obtener_por_id({"id": session["usuario_id"]})

    data = {
        "usuario": usuario,
        "citas_pendientes": Cita.pendientes_usuario({"usuario_id": usuario.id}),
        "proxima_cita": Cita.proxima({"usuario_id": usuario.id}),
        "pedidos_en_curso": Pedido.en_curso({"usuario_id": usuario.id}),
        "ultimas_citas": Cita.ultimas_usuario({"usuario_id": usuario.id}),
        "ultimos_pedidos": Pedido.ultimos({"usuario_id": usuario.id})
    }

    return render_template("usuario.html", **data)


# CRUD ADMIN DE USUARIOS


@app.route('/admin/usuarios')
def admin_lista_usuarios():

    if not is_admin():
        flash("No tienes permisos para acceder", "error")
        return redirect('/login')

    usuarios = Usuario.obtener_todos()

    return render_template("admin_usuarios.html", usuarios=usuarios)


@app.route('/admin/usuarios/nuevo')
def admin_nuevo_usuario():

    if not is_admin():
        return redirect('/login')

    return render_template("admin_usuario_nuevo.html")


@app.route('/admin/usuarios/crear', methods=['POST'])
def admin_crear_usuario():

    if not is_admin():
        return redirect('/login')

    pw_hash = bcrypt.generate_password_hash(request.form["password"])

    data = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"],
        "telefono": request.form["telefono"],
        "password": pw_hash,
        "rol": request.form["rol"]
    }

    Usuario.crear(data)

    flash("Usuario creado correctamente", "success")
    return redirect('/admin/usuarios')


@app.route('/admin/usuarios/editar/<int:id>')
def admin_editar_usuario(id):

    if not is_admin():
        return redirect('/login')

    usuario = Usuario.obtener_por_id({"id": id})

    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect('/admin/usuarios')

    return render_template("admin_usuario_editar.html", usuario=usuario)


@app.route('/admin/usuarios/actualizar/<int:id>', methods=['POST'])
def admin_actualizar_usuario(id):

    if not is_admin():
        return redirect('/login')

    data = {
        "id": id,
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"],
        "telefono": request.form["telefono"],
        "rol": request.form["rol"],
    }

    Usuario.actualizar(data)

    flash("Usuario actualizado correctamente", "success")
    return redirect('/admin/usuarios')


@app.route('/admin/usuarios/eliminar/<int:id>', methods=['POST'])
def admin_eliminar_usuario(id):

    if not is_admin():
        return redirect('/login')

    Usuario.eliminar({"id": id})

    flash("Usuario eliminado correctamente", "success")
    return redirect('/admin/usuarios')


# LOGOUT


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
