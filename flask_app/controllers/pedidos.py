from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.pedido import Pedido


@app.route('/carrito')
def carrito():
    return "Mi carrito de compras"


@app.route('/carrito/agregar/<int:id>')
def agregar_carrito(id):
    return f"Producto {id} agregado"


@app.route('/checkout')
def checkout():
    return "Página de pago"


@app.route('/checkout/procesar', methods=['POST'])
def procesar_pago():
    return "Procesando compra"
