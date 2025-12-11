// FUNCION PARA APLICAR COLOR AL SELECT

function aplicarColor(select) {


    select.classList.remove(
        "estado-pendiente",
        "estado-encamino",
        "estado-entregado"
    );

    const estado = select.value;

    if (estado === "pendiente") {
        select.classList.add("estado-pendiente");
    }
    if (estado === "en_camino") {
        select.classList.add("estado-encamino");
    }
    if (estado === "entregado") {
        select.classList.add("estado-entregado");
    }
}


// APLICAR COLOR AL CARGAR

document.querySelectorAll(".estado-select").forEach(select => {

    aplicarColor(select);

    select.addEventListener("change", function () {

        aplicarColor(this);

        const pedido_id = this.dataset.id;
        const nuevo_estado = this.value;

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