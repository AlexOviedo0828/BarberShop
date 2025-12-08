// Limpiar campos del registro al cargar
document.addEventListener("DOMContentLoaded", () => {
    const campos = ["nombre", "apellido", "email", "telefono", "password"];

    campos.forEach(id => {
        const input = document.getElementById(id);
        if (input) input.value = "";
    });
});

// Limpiar después del submit
const formRegistro = document.getElementById("formRegistro");

if (formRegistro) {
    formRegistro.addEventListener("submit", () => {
        const campos = ["nombre", "apellido", "email", "telefono", "password"];

        campos.forEach(id => {
            document.getElementById(id).value = "";
        });
    });
}