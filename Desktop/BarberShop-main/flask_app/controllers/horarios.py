from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.horario_barbero import HorarioBarbero
from flask_app.models.peluquero import Peluquero


def is_admin():
    return 'usuario_id' in session and session.get('rol') == 'admin'


@app.route("/admin/horarios")
def admin_horarios():
    if not is_admin():
        flash("No tienes permisos para acceder a esta sección", "danger")
        return redirect("/")

    horarios = HorarioBarbero.get_all_with_barbero()
    barberos = Peluquero.obtener_todos()

    return render_template(
        "admin_horarios.html",
        horarios=horarios,
        barberos=barberos
    )


@app.route("/admin/horarios/crear", methods=["POST"])
def crear_horario():
    if not is_admin():
        return redirect("/")
    if not HorarioBarbero.validate(request.form):
        return redirect(url_for("admin_horarios"))
    data = {
        "barbero_id": request.form["barbero_id"],
        "dia": request.form["dia"],
        "hora_inicio": request.form["hora_inicio"],
        "hora_fin": request.form["hora_fin"],
        "descanso_inicio": request.form.get("descanso_inicio") or None,
        "descanso_fin": request.form.get("descanso_fin") or None
    }
    HorarioBarbero.save(data)
    flash("Horario creado correctamente", "success")
    return redirect(url_for("admin_horarios"))


@app.route("/admin/horarios/actualizar/<int:id>", methods=["POST"])
def actualizar_horario(id):
    if not is_admin():
        return redirect("/")
    data = {
        "id": id,
        "barbero_id": request.form["barbero_id"],
        "dia": request.form["dia"],
        "hora_inicio": request.form["hora_inicio"],
        "hora_fin": request.form["hora_fin"],
        "descanso_inicio": request.form.get("descanso_inicio") or None,
        "descanso_fin": request.form.get("descanso_fin") or None
    }
    if not HorarioBarbero.validate(request.form):
        return redirect(url_for("admin_horarios"))
    HorarioBarbero.update(data)
    flash("Horario actualizado correctamente", "success")
    return redirect(url_for("admin_horarios"))


@app.route("/admin/horarios/eliminar/<int:id>", methods=["POST"])
def eliminar_horario(id):
    if not is_admin():
        return redirect("/")
    HorarioBarbero.delete({"id": id})
    flash("Horario eliminado", "success")
    return redirect(url_for("admin_horarios"))
