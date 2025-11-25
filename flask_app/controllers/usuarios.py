from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# login


@app.route('/')
@app.route('/login')
def login_form():
    return render_template('login.html')


@app.route('/login/procesar', methods=['POST'])
def login_procesar():
    email = request.form['email']
    password = request.form['password']

    # Validar
    if len(email) == 0 or len(password) == 0:
        flash("Todos los campos son obligatorios", "error")
        return redirect('/login')

    # Buscar usuario
    data = {"email": email}
    usuario = Usuario.obtener_por_email(data)

    if not usuario:
        flash("El usuario no existe", "error")
        return redirect('/login')

    # Validar contraseña
    if not bcrypt.check_password_hash(usuario.password, password):
        flash("Contraseña incorrecta", "error")
        return redirect('/login')

    # Guardar sesión
    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    session['rol'] = usuario.rol

    # Redirección según rol que se logea  el admin es alex@barber.cl y el password es 123456789
    if usuario.rol == "admin":
        return redirect('/dashboard/admin')

    return redirect('/dashboard/usuario')


# Registro

@app.route('/registro')
def registro_form():
    return render_template('registro.html')


@app.route('/registro/procesar', methods=['POST'])
def registro_procesar():

    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    telefono = request.form['telefono']
    password = request.form['password']
    password2 = request.form['password2']

    # Validaciones
    if len(nombre) < 2:
        flash("El nombre debe tener mínimo 2 caracteres", "error")
        return redirect('/registro')

    if len(apellido) < 2:
        flash("El apellido debe tener mínimo 2 caracteres", "error")
        return redirect('/registro')

    if len(email) < 5:
        flash("El correo no es válido", "error")
        return redirect('/registro')

    if password != password2:
        flash("Las contraseñas no coinciden", "error")
        return redirect('/registro')

    if len(password) < 6:
        flash("La contraseña debe tener al menos 6 caracteres", "error")
        return redirect('/registro')

    # Verificar correo ya registrado
    existente = Usuario.obtener_por_email({"email": email})
    if existente:
        flash("Este correo ya está registrado", "error")
        return redirect('/registro')

    # Crear usuario
    pw_hash = bcrypt.generate_password_hash(password)

    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "password": pw_hash,
        "telefono": telefono,
        "rol": "usuario"
    }

    Usuario.crear(data)

    flash("Registro exitoso, ahora puedes iniciar sesión", "success")
    return redirect('/login')


# usuario

@app.route('/dashboard/usuario')
def dashboard_usuario():
    if 'usuario_id' not in session:
        return redirect('/login')

    if session.get('rol') != 'usuario':
        return redirect('/dashboard/admin')

    return render_template('usuario.html')

# cerrar session


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
