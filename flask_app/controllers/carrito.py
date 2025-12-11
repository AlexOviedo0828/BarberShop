from flask_app import app
from flask import render_template, request, redirect, session, jsonify
from flask_app.models.producto import Producto
from flask_app.models.pedido import Pedido
from flask_app.models.detalle_pedido import DetallePedido


# =============================
#   INICIALIZAR CARRITO
# =============================

def init_carrito():
    if "carrito" not in session:
        session["carrito"] = []


# =============================
#   TIENDA
# =============================

@app.route("/tienda")
def tienda():
    productos = Producto.obtener_todos()
    return render_template("usuario_tienda.html", productos=productos)


# =============================
#   AGREGAR AL CARRITO
# =============================

@app.route("/carrito/agregar", methods=["POST"])
def carrito_agregar():
    init_carrito()

    data = request.json
    producto_id = data["id"]
    nombre = data["nombre"]
    precio = float(data["precio"])
    img = data["img"]

    session["carrito"].append({
        "id": producto_id,
        "nombre": nombre,
        "precio": precio,
        "img": img,
        "cantidad": 1
    })

    session.modified = True
    return jsonify({"status": "ok", "msg": "Producto agregado"})


# =============================
#   ELIMINAR PRODUCTO
# =============================

@app.route("/carrito/eliminar/<int:index>", methods=["POST"])
def carrito_eliminar(index):
    init_carrito()

    if 0 <= index < len(session["carrito"]):
        session["carrito"].pop(index)
        session.modified = True

    return jsonify({"status": "ok"})


# =============================
#   VACIAR CARRITO
# =============================

@app.route("/carrito/vaciar", methods=["POST"])
def carrito_vaciar():
    session["carrito"] = []
    session.modified = True
    return jsonify({"status": "ok"})


# =============================
#   CHECKOUT (CORREGIDO)
# =============================

@app.route("/carrito/checkout", methods=["POST"])
def carrito_checkout():

    init_carrito()

    print("SESSION CARRITO:", session.get("carrito"))  # <-- DEBUG

    if "usuario_id" not in session:
        return jsonify({"error": "Debes iniciar sesión para comprar"}), 401

    carrito = session["carrito"]

    if len(carrito) == 0:
        return jsonify({"error": "El carrito está vacío"}), 400

    data = request.json
    print("JSON RECIBIDO CHECKOUT:", data)  # <-- DEBUG

    total = sum(item["precio"] * item["cantidad"] for item in carrito)

    # Crear pedido CORRECTAMENTE
    pedido_id = Pedido.crear({
        "usuario_id": session["usuario_id"],
        "total": total,
        "estado": "pendiente",
        "direccion_envio": data.get("direccion_envio"),
        "metodo_pago": data.get("metodo_pago")
    })

    # Crear detalles
    for item in carrito:
        DetallePedido.crear({
            "pedido_id": pedido_id,
            "producto_id": item["id"],
            "cantidad": item["cantidad"],
            "precio": item["precio"]
        })

    # Vaciar carrito backend
    session["carrito"] = []
    session.modified = True

    return jsonify({
        "status": "ok",
        "pedido_id": pedido_id,
        "msg": "Pedido realizado con éxito"
    })
