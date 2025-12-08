/* =======================================================
   🛒 CARRITO PROFESIONAL – BARBERSHOP
======================================================= */

let carrito = [];

/* =======================================================
   🔄 Cargar carrito desde localStorage
======================================================= */
document.addEventListener("DOMContentLoaded", () => {
    const guardado = localStorage.getItem("carrito");
    if (guardado) carrito = JSON.parse(guardado);
    renderCarrito();
});

/* =======================================================
   💾 Guardar en localStorage
======================================================= */
function guardarCarrito() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
}

/* =======================================================
   🟢 Mostrar/Ocultar Carrito
======================================================= */
function toggleCarrito() {
    document.getElementById("carrito-panel").classList.toggle("active");
}

/* =======================================================
   🛠 Agregar producto al carrito
======================================================= */
document.querySelectorAll(".btn-add").forEach(btn => {
    btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        const nombre = btn.dataset.nombre;
        const precio = Number(btn.dataset.precio);
        const img = btn.dataset.img;

        const existente = carrito.find(p => p.id === id);

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
   📦 Renderizar carrito
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
   🔢 Cambiar cantidad
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
   ❌ Eliminar producto
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
   🛍 FINALIZAR COMPRA (FUNCIONANDO)
======================================================= */
function checkout() {

    if (carrito.length === 0) {
        return Swal.fire("Carrito vacío", "Agrega productos primero", "warning");
    }

    let resumen = `
        <div style="text-align:left;">
            <h4>Resumen de tu pedido:</h4>
            <hr>
    `;

    carrito.forEach(item => {
        resumen += `
            <p><strong>${item.nombre}</strong> x${item.cantidad}  
            — $${(item.precio * item.cantidad).toLocaleString()}</p>
        `;
    });

    resumen += `
            <hr>
            <h3>Total: $${carrito.reduce((t, p) => t + p.precio * p.cantidad, 0).toLocaleString()}</h3>
        </div>
    `;

    Swal.fire({
        title: "Confirmar compra",
        html: resumen,
        icon: "info",
        showCancelButton: true,
        confirmButtonText: "Realizar compra",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "#00e676"
    }).then(async res => {

        if (!res.isConfirmed) return;

        const response = await fetch("/finalizar_compra", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                carrito
            })
        });

        const data = await response.json();

        if (!data.success || !data.pedido_id || data.pedido_id <= 0) {
            return Swal.fire("Error", "No se pudo procesar la compra", "error");
        }

        // 🔥 Limpiar carrito después de compra
        carrito = [];
        guardarCarrito();
        renderCarrito();

        // Cerrar panel carrito
        document.getElementById("carrito-panel").classList.remove("active");

        // Mostrar confirmación + botón correcto
        Swal.fire({
            icon: "success",
            title: "Compra realizada",
            html: `
                <p>Pedido #${data.pedido_id} creado con éxito</p>
                <a href="/compra_exitosa/${data.pedido_id}" 
                   class="btn btn-success">
                    Ver pedido
                </a>
            `,
            showConfirmButton: false
        });
    });
}