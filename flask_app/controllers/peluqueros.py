from flask_app import app
from flask import render_template, request, redirect, flash
from flask_app.models.peluquero import Peluquero


@app.route('/admin/peluqueros')
def listar_peluqueros():
    peluqueros=Peluquero.get_all()
    print(f'\n\nPELQUEROS: {peluqueros}\n\n')
    return render_template('admin_peluqueros.html', peluqueros=peluqueros)


@app.route('/admin/peluqueros/nuevo')
def nuevo_peluquero():
    return render_template('admin_peluquero_nuevo.html')


@app.route('/admin/peluquero/crear', methods=['POST'])
def crear_peluquero():
    data={
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'telefono': request.form['telefono'],
        'especialidad': request.form['especialidad'],
        'imagen': None,
        'servicios_realizados': None
    }
    if data['especialidad']=="":
        data['especialidad'] = None

    Peluquero.insert(data)
    flash("Peluquero creado correctamente", "success")
    return redirect('/admin/peluqueros')


@app.route('/admin/peluqueros/editar/<int:id>')
def editar_peluquero(id):
    datos={'id': id}
    return render_template('admin_peluquero_editar.html', peluquero=Peluquero.obtener_por_id(datos))


@app.route('/admin/peluqueros/actualizar/<int:id>', methods=['POST'])
def actualizar_peluquero(id):
    datos={
        'id': id,
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'telefono': request.form['telefono'],
        'especialidad': request.form['especialidad'],
        'imagen': None,
        'servicios_realizados': None,
        'disponible': request.form['disponible']
    }
    Peluquero.update(datos)
    flash("Peluquero actualizado correctamente", "success")
    return redirect('/admin/peluqueros')


@app.route('/admin/peluqueros/eliminar/<int:id>', methods=['POST'])
def eliminar_peluquero(id):
    datos={'id': id}
    Peluquero.delete(datos)
    flash("Peluquero eliminado correctamente", "success")
    return redirect('/admin/peluqueros')