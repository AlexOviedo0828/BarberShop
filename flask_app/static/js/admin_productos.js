function filtrarProductos() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let cards = document.querySelectorAll(".product-card");

    cards.forEach(card => {
        let nombre = card.querySelector(".product-name").textContent.toLowerCase();

        if (nombre.includes(input)) {
            card.parentElement.style.display = "";
        } else {
            card.parentElement.style.display = "none";
        }
    });
}