from flask import render_template, request, redirect, session, flash, jsonify, make_response
from flask_app import app
from flask_app.models.pedido import Pedido
from flask_app.models.detalle_pedido import DetallePedido
from flask_app.models.producto import Producto

import pdfkit

path_wkhtmltopdf = "/usr/local/bin/wkhtmltopdf"

config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

#  CREAR PEDIDO DESDE EL CARRITO


@app.post("/crear_pedido")
def crear_pedido():
    if "usuario_id" not in session:
        return jsonify({"status": "error", "message": "Debes iniciar sesión"}), 403

    data = request.json
    carrito = data.get("carrito", [])
    direccion = data.get("direccion", "")
    metodo = data.get("metodo", "efectivo")

    if not carrito:
        return jsonify({"status": "error", "message": "Carrito vacío"}), 400

    total = sum(item["precio"] * item["cantidad"] for item in carrito)

    pedido_id = Pedido.crear({
        "usuario_id": session["usuario_id"],
        "total": total,
        "estado": "pendiente",
        "direccion": direccion,
        "metodo_pago": metodo,
    })

    for item in carrito:
        DetallePedido.crear({
            "pedido_id": pedido_id,
            "producto_id": item["id"],
            "cantidad": item["cantidad"],
            "precio": item["precio"],
        })

    return jsonify({"status": "success", "pedido_id": pedido_id})


#  COMPRA EXITOSA

@app.get("/compra_exitosa/<int:pedido_id>")
def compra_exitosa(pedido_id):
    pedido = Pedido.obtener_por_id({"id": pedido_id})
    if not pedido:
        flash("El pedido no existe", "error")
        return redirect("/mis_pedidos")

    detalles = DetallePedido.obtener_por_pedido({"pedido_id": pedido_id})

    return render_template(
        "compra_exitosa.html",
        pedido=pedido,
        detalles=detalles
    )


# MIS PEDIDOS

@app.get("/mis_pedidos")
def mis_pedidos():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión", "error")
        return redirect("/login")

    pedidos = Pedido.ultimos({"usuario_id": session["usuario_id"]})
    return render_template("mis_pedidos.html", pedidos=pedidos)


# DETALLE INDIVIDUAL DEL PEDIDO

@app.get("/pedido/<int:pedido_id>/detalle")
def pedido_detalle(pedido_id):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión", "error")
        return redirect("/login")

    pedido = Pedido.obtener_por_id({"id": pedido_id})
    if not pedido:
        flash("El pedido no existe", "error")
        return redirect("/mis_pedidos")

    detalles = DetallePedido.obtener_por_pedido({"pedido_id": pedido_id})

    return render_template(
        "detalle_pedido.html",
        pedido=pedido,
        detalles=detalles
    )


#  PDF DEL PEDIDO

@app.route('/pedido/<int:id>/pdf')
def pedido_pdf(id):

    pedido = Pedido.obtener_por_id({"id": id})
    detalles = DetallePedido.obtener_por_pedido({"pedido_id": id})

    html = render_template("pedido_pdf.html", pedido=pedido, detalles=detalles)

    pdf = pdfkit.from_string(html, False, configuration=config, options={
        "enable-local-file-access": None
    })

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=pedido_{id}.pdf'

    return response

    @classmethod
    def obtener_por_pedido(cls, data):
        query = """
        SELECT dp.id, dp.pedido_id, dp.producto_id, dp.cantidad, dp.precio,
               p.nombre AS producto_nombre,
               p.imagen AS producto_imagen
        FROM detalles_pedido dp
        JOIN productos p ON p.id = dp.producto_id
        WHERE dp.pedido_id = %(pedido_id)s;
    """

        results = connectToMySQL(cls.db).query_db(query, data)

        detalles = []
        if results:
            for row in results:
                det = cls(row)
                det.producto_nombre = row["producto_nombre"]
                det.producto_imagen = row["producto_imagen"]
                detalles.append(det)

        return detalles
