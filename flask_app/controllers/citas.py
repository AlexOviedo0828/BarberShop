from datetime import datetime, timedelta, date
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.cita import Cita
from flask_app.models.peluquero import Peluquero


def obtener_semana(fecha: date):
    inicio = fecha - timedelta(days=fecha.weekday())  # lunes
    fin = inicio + timedelta(days=6)
    return inicio, fin


@app.route('/citas/mis-citas')
def mis_citas_usuario():
    if "usuario_id" not in session:
        return redirect("/logout")

    data = {"usuario_id": session["usuario_id"]}

    proxima_cita = Cita.proxima(data)
    citas_pendientes = Cita.pendientes_usuario(data)

    return render_template(
        "mis_citas.html",
        proxima_cita=proxima_cita,
        citas_pendientes=citas_pendientes
    )


@app.route('/citas/agendar')
def agendar_cita():
    if "usuario_id" not in session:
        return redirect("/logout")

    peluqueros = Peluquero.obtener_todos()
    peluquero_id = request.args.get("peluquero_id", type=int)

    if not peluquero_id:
        return render_template("citas_semanal.html", peluqueros=peluqueros)

    peluquero = Peluquero.obtener_por_id({"id": peluquero_id})

    hoy = datetime.now().date()
    inicio_semana, fin_semana = obtener_semana(hoy)

    dias_es = ["Lunes", "Martes", "Miércoles",
               "Jueves", "Viernes", "Sábado", "Domingo"]
    dias = []

    for i in range(7):
        fecha = inicio_semana + timedelta(days=i)
        fecha_str = fecha.strftime("%Y-%m-%d")

        horas = []
        for h in range(8, 18):  # 8am–5pm
            hora_txt = f"{h:02d}:00"

            ocupado = Cita.existe_solapamiento({
                "peluquero_id": peluquero_id,
                "fecha": fecha_str,
                "hora": hora_txt,
                "duracion_minutos": 30
            })

            horas.append({
                "hora": hora_txt,
                "ocupado": ocupado
            })

        dias.append({
            "fecha": fecha_str,
            "dia": dias_es[i],
            "horas": horas
        })

    semana = {
        "inicio": inicio_semana.strftime("%Y-%m-%d"),
        "fin": fin_semana.strftime("%Y-%m-%d"),
        "dias": dias
    }

    return render_template(
        "citas_semanal.html",
        peluqueros=peluqueros,
        peluquero=peluquero,
        semana=semana
    )


@app.route('/citas/agendar/procesar', methods=['POST'])
def procesar_cita():
    if "usuario_id" not in session:
        return redirect("/logout")

    data = {
        "usuario_id": session["usuario_id"],
        "peluquero_id": request.form["peluquero_id"],
        "fecha": request.form["fecha"],
        "hora": request.form["hora"],
        "estado": "pendiente",
        "notas": request.form.get("notas", ""),
        "duracion_minutos": 30
    }

    if not data["fecha"] or not data["hora"]:
        flash("Debe seleccionar fecha y hora", "error")
        return redirect(f"/citas/agendar?peluquero_id={data['peluquero_id']}")

    if Cita.existe_solapamiento(data):
        flash("El barbero ya tiene una cita en ese horario", "error")
        return redirect(f"/citas/agendar?peluquero_id={data['peluquero_id']}")

    Cita.crear(data)
    flash("Cita creada correctamente", "success")
    return redirect("/citas/mis-citas")


@app.route('/citas/cancelar/<int:id>')
def cancelar_cita(id):
    if "usuario_id" not in session:
        return redirect("/logout")

    Cita.cancelar({
        "id": id,
        "motivo": "Cancelada por el usuario"
    })

    flash("La cita ha sido cancelada", "success")
    return redirect("/citas/mis-citas")


@app.route('/citas')
def citas_redirect():
    return redirect('/citas/mis-citas')
