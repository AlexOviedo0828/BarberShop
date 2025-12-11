function filtrarProductos() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const productos = document.querySelectorAll("#productosContainer .product-item");

    productos.forEach(producto => {
        const nombre = producto.querySelector(".product-name").innerText.toLowerCase();

        if (nombre.includes(input)) {
            producto.style.display = "block";
            producto.style.opacity = "1";
            producto.style.transform = "scale(1)";
        } else {
            producto.style.opacity = "0";
            producto.style.transform = "scale(0.9)";
            setTimeout(() => {
                producto.style.display = "none";
            }, 200);
        }
    });
}

/* =======================================================
   🛒 CARRITO LOCAL (localStorage)
======================================================= */
let carrito = [];

document.addEventListener("DOMContentLoaded", () => {
    const guardado = localStorage.getItem("carrito");
    if (guardado) carrito = JSON.parse(guardado);

    renderCarrito();
});

/* =======================================================
   💾 Guardar carrito local
======================================================= */
function guardarCarrito() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
}

/* =======================================================
   🎚 Mostrar/Ocultar panel del carrito
======================================================= */
function toggleCarrito() {
    document.getElementById("carrito-panel").classList.toggle("active");
}

/* =======================================================
   ➕ Agregar producto al carrito
======================================================= */
document.querySelectorAll(".btn-add").forEach(btn => {
    btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        const nombre = btn.dataset.nombre;
        const precio = Number(btn.dataset.precio);
        const img = btn.dataset.img;

        const existente = carrito.find(p => p.id == id);

        if (existente) {
            existente.cantidad++;
        } else {
            carrito.push({
                id,
                nombre,
                precio,
                img,
                cantidad: 1
            });
        }

        guardarCarrito();
        renderCarrito();

        Swal.fire({
            icon: "success",
            title: "Producto agregado",
            text: nombre + " añadido al carrito",
            timer: 1200,
            showConfirmButton: false
        });
    });
});

/* =======================================================
   🧮 Renderizar carrito en el panel
======================================================= */
function renderCarrito() {
    const container = document.getElementById("carrito-items");
    const badge = document.getElementById("carrito-count");

    container.innerHTML = "";
    let total = 0;

    carrito.forEach((p, index) => {
        const subtotal = p.precio * p.cantidad;
        total += subtotal;

        container.innerHTML += `
            <div class="carrito-item">
                <img class="carrito-img" src="/static/img/productos/${p.img}" />

                <div class="carrito-info">
                    <h6>${p.nombre}</h6>
                    <p class="precio">$ ${p.precio.toLocaleString()}</p>
                    <p class="subtotal">Subtotal: $ ${subtotal.toLocaleString()}</p>

                    <div class="quantity-box">
                        <button onclick="cambiarCantidad(${index}, -1)">−</button>
                        <span>${p.cantidad}</span>
                        <button onclick="cambiarCantidad(${index}, 1)">+</button>
                    </div>
                </div>

                <button class="btn-delete" onclick="eliminar(${index})">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        `;
    });

    badge.innerText = carrito.reduce((s, p) => s + p.cantidad, 0);
    document.getElementById("carrito-total").innerText = total.toLocaleString();

    guardarCarrito();
}

/* =======================================================
   🔢 Cambiar cantidad de un producto
======================================================= */
function cambiarCantidad(index, cambio) {
    carrito[index].cantidad += cambio;

    if (carrito[index].cantidad <= 0) {
        eliminar(index);
        return;
    }

    guardarCarrito();
    renderCarrito();
}

/* =======================================================
   ❌ Eliminar un producto del carrito
======================================================= */
function eliminar(index) {
    Swal.fire({
        title: "¿Eliminar producto?",
        text: "Se quitará del carrito",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "#d33"
    }).then(res => {
        if (res.isConfirmed) {
            carrito.splice(index, 1);
            renderCarrito();
        }
    });
}

/* =======================================================
   🔄 Sincronizar carrito local → backend (SESSION)
======================================================= */
async function sincronizarCarritoBackend() {
    await fetch("/carrito/vaciar", {
        method: "POST"
    }); // Reiniciamos el carrito del backend

    for (let item of carrito) {
        await fetch("/carrito/agregar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: item.id,
                nombre: item.nombre,
                precio: item.precio,
                img: item.img
            })
        });
    }
}

/* =======================================================
   🧾 CHECKOUT PRO — SweetAlert2
======================================================= */
function checkout() {
    if (carrito.length === 0) {
        Swal.fire("Carrito vacío", "Agrega productos antes de comprar", "warning");
        return;
    }

    let resumen = carrito.map(p => `
        <div class="swal-item">
            <img src="/static/img/productos/${p.img}" class="swal-thumb">
            <div>
                <strong>${p.nombre}</strong><br>
                Cant: ${p.cantidad} — 
                <span class="swal-price">$${(p.precio * p.cantidad).toLocaleString()}</span>
            </div>
        </div>
    `).join("");

    let total = carrito.reduce((acc, p) => acc + (p.precio * p.cantidad), 0);

    Swal.fire({
        title: "🛒 Confirmar compra",
        width: 600,
        background: "#1e1e1e",
        color: "#fff",
        html: `
            <style>
                .swal-item { display:flex; gap:12px; margin-bottom:10px; }
                .swal-thumb { width:50px; height:50px; object-fit:cover; border-radius:8px;}
                .swal-price { color:#06d6a0; }
                .swal2-input { background:#2b2b2b !important; color:white !important; }
            </style>

            <h5>🧾 Resumen:</h5>
            <div style="max-height:160px; overflow-y:auto;">${resumen}</div>

            <hr>

            <h4 class="swal-price">Total: $${total.toLocaleString()}</h4>

            <hr>

            <label>📍 Dirección de envío</label>
            <input id="direccion_envio" class="swal2-input" placeholder="Ej: Calle 123">

            <label>📞 Teléfono</label>
            <input id="telefono" class="swal2-input" placeholder="Ej: +56 9 1234 5678">

            <label>💳 Método de pago</label>
            <select id="metodo_pago" class="swal2-input">
                <option value="" disabled selected>Seleccionar...</option>
                <option value="Efectivo">Efectivo</option>
                <option value="Transferencia">Transferencia</option>
            </select>
        `,
        showCancelButton: true,
        confirmButtonText: "Pagar ahora 💵",
        cancelButtonText: "Cancelar",
        preConfirm: () => {
            const direccion = document.getElementById("direccion_envio").value.trim();
            const telefono = document.getElementById("telefono").value.trim();
            const metodo = document.getElementById("metodo_pago").value.trim();

            if (!direccion || !telefono || !metodo) {
                Swal.showValidationMessage("⚠ Debes completar todos los campos");
                return false;
            }

            return {
                direccion_envio: direccion,
                telefono,
                metodo_pago: metodo
            };
        }
    }).then(async result => {
        if (result.isConfirmed) {

            await sincronizarCarritoBackend();

            fetch("/carrito/checkout", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(result.value)
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === "ok") {
                        Swal.fire({
                            icon: "success",
                            title: "Compra realizada 🎉",
                            text: "Tu pedido fue registrado exitosamente",
                            background: "#1e1e1e",
                            color: "#fff"
                        });

                        carrito = [];
                        guardarCarrito();
                        renderCarrito();
                    }
                });
        }
    });
}