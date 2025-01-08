document.addEventListener("DOMContentLoaded", function () {
    // Botones para agregar al carrito
    const addToCartButtons = document.querySelectorAll(".add-to-cart");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Prevenir el comportamiento por defecto

            const peliculaId = this.dataset.peliculaId;
            const url = `/carro/agregar/${peliculaId}/`;

            // Enviar la petición AJAX
            fetch(url, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCSRFToken(), // Función para obtener el token CSRF
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Actualizar el carrito dinámicamente
                        updateCartUI();
                        showToast(data.message); // Mostrar un mensaje (opcional)
                    } else {
                        showToast(data.message, "error"); // Mostrar error
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    });

    // Función para obtener el token CSRF
    function getCSRFToken() {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        return csrfToken;
    }

    // Función para actualizar el carrito (puedes implementarla según tu necesidad)
    function updateCartUI() {
        // Aquí puedes hacer una nueva petición al servidor para obtener el contenido actualizado del carrito
        fetch("/carro/ver/")
            .then(response => response.text())
            .then(html => {
                document.querySelector("#carro-container").innerHTML = html;
            });
    }

    // Función para mostrar mensajes (opcional)
    function showToast(message, type = "success") {
        // Implementa tu lógica para mostrar mensajes en pantalla
        console.log(`[${type.toUpperCase()}]: ${message}`);
    }
});
