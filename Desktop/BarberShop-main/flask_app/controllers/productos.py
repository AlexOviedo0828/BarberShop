from flask_app import app
from flask import render_template, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename
import os

from flask_app.models.producto import Producto
from flask_app.models.categoria import Categoria

# esto permite subir las imagenes en los formatos para poder cargarlas Angel...
UPLOAD_FOLDER = os.path.join(os.getcwd(), "flask_app/static/img/peluqueros")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# LISTAR PRODUCTOS


@app.route('/admin/productos')
def admin_productos():
    productos = Producto.obtener_todos()
    return render_template("admin_productos.html", productos=productos)


# FORMULARIO NUEVO

@app.route('/admin/productos/nuevo')
def nuevo_producto():
    categorias = Categoria.obtener_todas()  # opcional
    return render_template("admin_productos_nuevo.html", categorias=categorias)


# CREAR PRODUCTO (POST)

@app.route('/admin/productos/crear', methods=['POST'])
def crear_producto():

    imagen = request.files.get("imagen")
    filename = None

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    else:
        flash("Imagen inválida", "error")

    data = {
        "nombre": request.form["nombre"],
        "descripcion": request.form["descripcion"],
        "precio": request.form["precio"],
        "stock": request.form["stock"],
        "categoria_id": request.form["categoria_id"],
        "imagen": filename
    }

    Producto.crear(data)

    flash("Producto creado correctamente", "success")
    return redirect("/admin/productos")


# FORMULARIO EDITAR

@app.route('/admin/productos/editar/<int:id>')
def editar_producto(id):
    producto = Producto.obtener_por_id({"id": id})
    categorias = Categoria.obtener_todas()
    return render_template("admin_productos_editar.html", producto=producto, categorias=categorias)


# ACTUALIZAR PRODUCTO

@app.route('/admin/productos/actualizar/<int:id>', methods=['POST'])
def actualizar_producto(id):

    producto_actual = Producto.obtener_por_id({"id": id})

    imagen = request.files.get("imagen")

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # eliminar imagen anterior
        if producto_actual.imagen:
            old = os.path.join(
                app.config["UPLOAD_FOLDER"], producto_actual.imagen)
            if os.path.exists(old):
                os.remove(old)
    else:
        filename = producto_actual.imagen

    data = {
        "id": id,
        "nombre": request.form["nombre"],
        "descripcion": request.form["descripcion"],
        "precio": request.form["precio"],
        "stock": request.form["stock"],
        "categoria_id": request.form["categoria_id"],
        "imagen": filename
    }

    Producto.actualizar(data)

    flash("Producto actualizado correctamente", "success")
    return redirect("/admin/productos")


# ELIMINAR PRODUCTO (SweetAlert)

@app.route('/admin/productos/eliminar/<int:id>', methods=["POST"])
def eliminar_producto(id):

    producto = Producto.obtener_por_id({"id": id})

    # borrar imagen
    if producto and producto.imagen:
        img_path = os.path.join(app.config["UPLOAD_FOLDER"], producto.imagen)
        if os.path.exists(img_path):
            os.remove(img_path)

    Producto.eliminar({"id": id})

    return jsonify({"status": "ok"})
