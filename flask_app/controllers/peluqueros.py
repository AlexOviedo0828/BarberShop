from flask_app import app
from flask import render_template, request, redirect, flash
from flask_app.models.peluquero import Peluquero
import os
import json


@app.route('/admin/peluqueros')
def listar_peluqueros():
    peluqueros = Peluquero.obtener_todos()   # ✅ CORREGIDO
    return render_template('admin_peluqueros.html', peluqueros=peluqueros)


@app.route('/admin/peluqueros/nuevo')
def nuevo_peluquero():
    return render_template('admin_peluquero_nuevo.html')


@app.route('/admin/peluquero/crear', methods=['POST'])
def crear_peluquero():

    imagen = request.files.get('imagen')
    nombre_archivo = None

    carpeta = "flask_app/static/img/peluqueros"
    os.makedirs(carpeta, exist_ok=True)

    if imagen and imagen.filename != "":
        nombre_archivo = imagen.filename.replace(" ", "_").lower()
        imagen.save(os.path.join(carpeta, nombre_archivo))

        imagen_json = json.dumps({
            "url": f"img/peluqueros/{nombre_archivo}"
        })
    else:
        imagen_json = None

    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "telefono": request.form['telefono'],
        "especialidad": request.form['especialidad'] or None,
        "imagen": imagen_json,
        "servicios_realizados": 0
    }

    Peluquero.insert(data)
    flash("Peluquero creado correctamente", "success")
    return redirect("/admin/peluqueros")


@app.route('/admin/peluqueros/editar/<int:id>')
def editar_peluquero(id):
    peluquero = Peluquero.obtener_por_id({"id": id})
    return render_template("admin_peluquero_editar.html", peluquero=peluquero)


@app.route('/admin/peluqueros/actualizar/<int:id>', methods=['POST'])
def actualizar_peluquero(id):

    peluquero_actual = Peluquero.obtener_por_id({"id": id})

    imagen = request.files.get("imagen")
    carpeta = "flask_app/static/img/peluqueros"

    if imagen and imagen.filename != "":
        nombre_archivo = imagen.filename.replace(" ", "_").lower()
        imagen.save(os.path.join(carpeta, nombre_archivo))

        imagen_json = json.dumps({
            "url": f"img/peluqueros/{nombre_archivo}"
        })
    else:
        imagen_json = json.dumps(
            peluquero_actual.imagen) if peluquero_actual.imagen else None

    data = {
        "id": id,
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "telefono": request.form['telefono'],
        "especialidad": request.form['especialidad'],
        "imagen": imagen_json,
        "servicios_realizados": peluquero_actual.servicios_realizados,
        "disponible": request.form['disponible']
    }

    Peluquero.update(data)
    flash("Peluquero actualizado correctamente", "success")
    return redirect("/admin/peluqueros")


@app.route('/admin/peluqueros/eliminar/<int:id>', methods=['POST'])
def eliminar_peluquero(id):
    Peluquero.delete({"id": id})
    flash("Peluquero eliminado correctamente", "success")
    return redirect("/admin/peluqueros")
