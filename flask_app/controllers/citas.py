from datetime import datetime, timedelta, date
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.cita import Cita
from flask_app.models.peluquero import Peluquero
from flask_app.models.horario_barbero import HorarioBarbero


def obtener_semana(fecha: date):
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday()) # Lunes
    return [inicio_semana + timedelta(days=i) for i in range(7)]



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

    # Si no se ha elegido barbero todavía
    if not peluquero_id:
        return render_template("citas_semanal.html", peluqueros=peluqueros)

    peluquero = Peluquero.obtener_por_id({"id": peluquero_id})

    # GENERA FECHAS DE LA SEMANA

    dias_semana = obtener_semana(datetime.now().date())
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"]

    semana = {}
    fechas = []

    for i, dia in enumerate(dias):
        fecha_real = dias_semana[i].strftime("%Y-%m-%d")
        fechas.append(fecha_real)

        # Horarios del barbero para ese día
        horarios = HorarioBarbero.get_by_barbero_and_dia({
            "barbero_id": peluquero_id,
            "dia": dia
        })

        # Agregamos la fecha a cada horario
        lista_horarios = []
        for horario in horarios:
            lista_horarios.append({
                "id": horario.id,
                "hora_inicio": horario.hora_inicio,
                "hora_fin": horario.hora_fin,
                "reservado": horario.reservado,
                "fecha": fecha_real
            })

        semana[dia] = lista_horarios


    # hoy = datetime.now().date()
    # inicio_semana, fin_semana = obtener_semana(hoy)

    # dias_es = ["Lunes", "Martes", "Miércoles",
    #            "Jueves", "Viernes", "Sábado", "Domingo"]
    # dias = []

    # for i in range(7):
    #     fecha = inicio_semana + timedelta(days=i)
    #     fecha_str = fecha.strftime("%Y-%m-%d")

    #     horas = []
    #     for h in range(8, 18):  # 8am–5pm
    #         hora_txt = f"{h:02d}:00"

    #         ocupado = Cita.existe_solapamiento({
    #             "peluquero_id": peluquero_id,
    #             "fecha": fecha_str,
    #             "hora": hora_txt,
    #             "duracion_minutos": 30
    #         })

    #         horas.append({
    #             "hora": hora_txt,
    #             "ocupado": ocupado
    #         })

    #     dias.append({
    #         "fecha": fecha_str,
    #         "dia": dias_es[i],
    #         "horas": horas
    #     })

    # semana = {
    #     "inicio": inicio_semana.strftime("%Y-%m-%d"),
    #     "fin": fin_semana.strftime("%Y-%m-%d"),
    #     "dias": dias
    # }

    return render_template(
        "citas_semanal.html",
        peluqueros=peluqueros,
        peluquero=peluquero,
        semana=semana,
        dias=dias,
        fechas=fechas,
        zip=zip
    )


@app.route('/citas/agendar/procesar', methods=['POST'])
def procesar_cita():
    if "usuario_id" not in session:
        return redirect("/logout")

    data = {
        "usuario_id": session["usuario_id"],
        "peluquero_id": request.form["peluquero_id"],
        "fecha": request.form["fecha"],
        "hora": f'{request.form["hora_inicio"]} - {request.form["hora_fin"]}',
        "estado": "pendiente",
        "horario_id": request.form["horario_id"],
        "notas": request.form.get("notas", ""),
    }

    # if not data["fecha"] or not data["hora"]:
    #     flash("Debe seleccionar fecha y hora", "error")
    #     return redirect(f"/citas/agendar?peluquero_id={data['peluquero_id']}")

    # if Cita.existe_solapamiento(data):
    #     flash("El barbero ya tiene una cita en ese horario", "error")
    #     return redirect(f"/citas/agendar?peluquero_id={data['peluquero_id']}")

    Cita.crear(data)
    
    HorarioBarbero.reservar({"id": request.form["horario_id"]})

    flash("Cita creada correctamente", "success")
    return redirect("/citas/mis-citas")


@app.route('/citas/cancelar/<int:id>')
def cancelar_cita(id):
    if "usuario_id" not in session:
        return redirect("/logout")
    
    cita = Cita.obtener_por_id({"id": id})

    Cita.cancelar({
        "id": id,
        "motivo": "Cancelada por el usuario"
    })

    HorarioBarbero.liberar({"id": cita.horario_id})

    flash("La cita ha sido cancelada", "success")
    return redirect("/citas/mis-citas")


@app.route('/citas')
def citas_redirect():
    return redirect('/citas/mis-citas')
