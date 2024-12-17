document.addEventListener("DOMContentLoaded", function () {
    // Selecciona todos los botones para agregar al carrito
    const botonesAgregarCarro = document.querySelectorAll(".btn-agregar-carro");

    botonesAgregarCarro.forEach(function (boton) {
        boton.addEventListener("click", function (e) {
            e.preventDefault(); // Evita que el formulario recargue la página

            const url = boton.getAttribute("data-url"); // URL del endpoint
            const peliculaId = boton.getAttribute("data-pelicula-id"); // ID de la película
            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // CSRF Token

            // Realiza la solicitud AJAX con fetch
            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ pelicula_id: peliculaId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    // Mostrar mensaje en el contenedor
                    const mensajeCarro = document.getElementById("mensaje-carro");
                    mensajeCarro.innerHTML = `<div class="alert alert-success">${data.message}</div>`;

                    // Actualizar el widget del carrito
                    actualizarWidgetCarro();
                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch(error => {
                console.error("Error al agregar la película:", error);
            });
        });
    });

    // Función para actualizar el widget del carrito
    function actualizarWidgetCarro() {
        fetch("{% url 'carro:widget' %}") // Asumiendo que tienes una URL para el widget
        .then(response => response.text())
        .then(data => {
            const widgetCarro = document.querySelector("#widget-carro"); // Asegúrate de tener este contenedor
            widgetCarro.innerHTML = data; // Actualiza el contenido del carrito
        });
    }
});
