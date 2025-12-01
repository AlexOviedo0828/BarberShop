from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt

from flask_app.models.usuario import Usuario
from flask_app.models.cita import Cita
from flask_app.models.pedido import Pedido

bcrypt = Bcrypt(app)


def is_admin():
    return "usuario_id" in session and session.get("rol") == "admin"


@app.route('/')
@app.route('/login')
def login_form():
    return render_template('login.html')


@app.route('/login/procesar', methods=['POST'])
def login_procesar():

    email = request.form['email']
    password = request.form['password']

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

    flash("Registro exitoso", "success")
    return redirect('/login')


@app.route('/dashboard/usuario')
def dashboard_usuario():

    if 'usuario_id' not in session:
        return redirect('/login')

    usuario_id = session["usuario_id"]

    citas_pendientes_list = Cita.pendientes_usuario({"usuario_id": usuario_id})
    citas_pendientes = len(citas_pendientes_list)
    proxima_cita = Cita.proxima({"usuario_id": usuario_id})
    ultimas_citas = Cita.ultimas_usuario({"usuario_id": usuario_id})

    pedidos_en_curso = Pedido.en_curso({"usuario_id": usuario_id})
    ultimos_pedidos = Pedido.ultimos({"usuario_id": usuario_id})

    usuario = Usuario.obtener_por_id({"id": usuario_id})
    nombre = usuario.nombre.capitalize()

    return render_template(
        "usuario.html",
        usuario=usuario,
        nombre=nombre,
        citas_pendientes=citas_pendientes,
        proxima_cita=proxima_cita,
        ultimas_citas=ultimas_citas,
        pedidos_en_curso=pedidos_en_curso,
        ultimos_pedidos=ultimos_pedidos
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
