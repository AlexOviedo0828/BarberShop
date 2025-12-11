// Limpiar inputs al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    const email = document.getElementById("email");
    const password = document.getElementById("password");

    if (email) email.value = "";
    if (password) password.value = "";
});

// Limpiar después de enviar el formulario
const formLogin = document.getElementById("formLogin");

if (formLogin) {
    formLogin.addEventListener("submit", () => {
        document.getElementById("email").value = "";
        document.getElementById("password").value = "";
    });
}