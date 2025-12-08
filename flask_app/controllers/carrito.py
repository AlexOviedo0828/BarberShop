from flask_app import app
from flask import render_template, request, redirect, session, jsonify
from flask_app.models.producto import Producto
from flask_app.models.pedido import Pedido
from flask_app.models.detalle_pedido import DetallePedido


# INICIALIZAR CARRITO

def init_carrito():
    if "carrito" not in session:
        session["carrito"] = []


# MOSTRAR TIENDA USUARIO

@app.route("/tienda")
def tienda():
    productos = Producto.obtener_todos()
    return render_template("usuario_tienda.html", productos=productos)


# AGREGAR PRODUCTO AL CARRITO (AJAX desde JS)

@app.route("/carrito/agregar", methods=["POST"])
def carrito_agregar():
    init_carrito()

    data = request.json

    producto_id = data["id"]
    nombre = data["nombre"]
    precio = float(data["precio"])
    img = data["img"]

    # Agregar al carrito como objeto
    session["carrito"].append({
        "id": producto_id,
        "nombre": nombre,
        "precio": precio,
        "img": img,
        "cantidad": 1
    })

    session.modified = True

    return jsonify({"status": "ok", "msg": "Producto agregado"})


# ELIMINAR PRODUCTO DEL CARRITO

@app.route("/carrito/eliminar/<int:index>", methods=["POST"])
def carrito_eliminar(index):
    init_carrito()

    if 0 <= index < len(session["carrito"]):
        session["carrito"].pop(index)
        session.modified = True

    return jsonify({"status": "ok", "msg": "Producto eliminado"})


# VACIAR CARRITO
@app.route("/carrito/vaciar", methods=["POST"])
def carrito_vaciar():
    session["carrito"] = []
    session.modified = True
    return jsonify({"status": "ok"})


# CHECKOUT (CREAR PEDIDO REAL EN BD)
@app.route("/carrito/checkout", methods=["POST"])
def carrito_checkout():

    init_carrito()

    if "usuario_id" not in session:
        return jsonify({"error": "Debes iniciar sesión para comprar"}), 401

    carrito = session["carrito"]

    if len(carrito) == 0:
        return jsonify({"error": "El carrito está vacío"}), 400

    total = sum(item["precio"] * item["cantidad"] for item in carrito)

    # Crear pedido en BD
    pedido_id = Pedido.crear({
        "usuario_id": session["usuario_id"],
        "total": total,
        "estado": "pendiente",
        "direccion": request.json.get("direccion", None),
        "metodo_pago": request.json.get("metodo_pago", None)
    })

    # Crear detalles del pedido
    for item in carrito:
        DetallePedido.crear({
            "pedido_id": pedido_id,
            "producto_id": item["id"],
            "cantidad": item["cantidad"],
            "precio": item["precio"]
        })

    # Vaciar carrito
    session["carrito"] = []
    session.modified = True

    return jsonify({
        "status": "ok",
        "pedido_id": pedido_id,
        "msg": "Pedido realizado con éxito"
    })


@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():

    data = request.get_json()
    carrito = data.get("carrito", [])

    if not carrito:
        return jsonify({"success": False, "msg": "Carrito vacío"})

    total = sum([float(p["precio"]) * int(p["cantidad"]) for p in carrito])

    pedido_data = {
        "usuario_id": session.get("usuario_id", 1),
        "total": total,
        "estado": "pendiente",
        "direccion": "No registrada",
        "metodo_pago": "Efectivo"
    }

    pedido_id = Pedido.crear(pedido_data)

    for p in carrito:
        DetallePedido.crear({
            "pedido_id": pedido_id,
            "producto_id": p["id"],
            "cantidad": p["cantidad"],
            "precio": p["precio"]
        })

    return jsonify({
        "success": True,
        "pedido_id": pedido_id
    })
