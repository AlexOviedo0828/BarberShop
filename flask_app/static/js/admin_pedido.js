// ==============================
// FUNCION PARA APLICAR COLOR AL SELECT
// ==============================
function aplicarColor(select) {
    // Quitamos clases previas
    select.classList.remove(
        "estado-pendiente",
        "estado-encamino",
        "estado-entregado"
    );

    // Asignamos color según estado
    if (select.value === "pendiente") {
        select.classList.add("estado-pendiente");
    }
    if (select.value === "encamino") {
        select.classList.add("estado-encamino");
    }
    if (select.value === "entregado") {
        select.classList.add("estado-entregado");
    }
}

// ==============================
// APLICAR COLOR AL CARGAR
// ==============================
document.querySelectorAll(".estado-select").forEach(select => {
    aplicarColor(select);

    // ==============================
    // EVENTO AL CAMBIAR EL SELECT
    // ==============================
    select.addEventListener("change", function () {
        aplicarColor(this);

        const pedido_id = this.dataset.id;
        const nuevo_estado = this.value;

        // Enviar actualización al backend
        fetch(`/admin/pedidos/estado/${pedido_id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    estado: nuevo_estado
                })
            })
            .then(res => res.json())
            .then(data => {
                console.log("Estado actualizado:", data);
            })
            .catch(err => console.error("Error:", err));
    });
});