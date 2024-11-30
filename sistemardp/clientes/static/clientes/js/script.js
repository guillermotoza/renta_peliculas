document.addEventListener('DOMContentLoaded', function() {
    const clientesList = document.getElementById('clientes-list');
    const clienteForm = document.getElementById('cliente-form');
    const editModal = document.getElementById('edit-modal');
    const closeButton = document.querySelector('.close-button');
    const editForm = document.getElementById('edit-form');
    let currentEditId = null;

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Cargar clientes
    function cargarClientes() {
        fetch('/clientes/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                clientesList.innerHTML = '';
                data.clientes.forEach(cliente => {
                    const clienteDiv = document.createElement('div');
                    clienteDiv.innerHTML = `
                        ${cliente.nombre} - ${cliente.correo} - ${cliente.direccion} - ${cliente.membresia}
                        <button onclick="editarCliente(${cliente.id})">Editar</button>
                        <button onclick="eliminarCliente(${cliente.id})">Eliminar</button>
                    `;
                    clientesList.appendChild(clienteDiv);
                });
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }

    cargarClientes();

    // Agregar cliente
    clienteForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(clienteForm);
        for (let [key, value] of formData.entries()) {
            console.log(key, value);  // Verifica los datos enviados
        }
        fetch('/clientes/agregar/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken  
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'Error desconocido');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                cargarClientes();
                clienteForm.reset();
            }
        })
        .catch(error => {
            console.error('Error al agregar cliente:', error);
            alert('Hubo un problema al agregar el cliente. Por favor, intenta nuevamente.');
        });
    });

    // Editar cliente
    window.editarCliente = function(clienteId) {
        currentEditId = clienteId;
        fetch(`/clientes/${clienteId}/editar/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('edit-nombre').value = data.nombre;
                document.getElementById('edit-correo').value = data.correo;
                document.getElementById('edit-direccion').value = data.direccion;
                document.getElementById('edit-membresia').value = data.membresia;
                editModal.style.display = 'block';
            });
    };

    editForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(editForm);
        fetch(`/clientes/${currentEditId}/editar/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken  
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                cargarClientes();
                editModal.style.display = 'none';
            }
        });
    });

    closeButton.addEventListener('click', function() {
        editModal.style.display = 'none';
    });

    window.eliminarCliente = function(clienteId) {
        if (confirm('¿Estás seguro de que deseas eliminar este cliente?')) {
            fetch(`/clientes/eliminar/${clienteId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken  
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    cargarClientes();
                }
            });
        }
    };
});