document.addEventListener('DOMContentLoaded', function() {
    const clienteForm = document.getElementById('cliente-form');
    const editForm = document.getElementById('edit-form');
    const editModal = document.getElementById('edit-modal');
    const closeButton = document.querySelector('.close-button');
    let currentEditId = null;

    // Cargar clientes al cargar la página
    fetchClientes();

    // Agregar cliente
    clienteForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(clienteForm);
        fetch('/usuario', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                agregarClienteALista(data);
                clienteForm.reset();
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Editar cliente
    editForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(editForm);
        fetch(`/clientes/${currentEditId}/editar/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                actualizarClienteEnLista(data);
                editModal.style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Cerrar modal de edición
    closeButton.addEventListener('click', function() {
        editModal.style.display = 'none';
    });

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

    // Función para cargar clientes
    function fetchClientes() {
        fetch('/clientes/')
        .then(response => response.json())
        .then(data => {
            const clientesList = document.getElementById('clientes-list');
            clientesList.innerHTML = '';
            data.clientes.forEach(cliente => {
                agregarClienteALista(cliente);
            });
        })
        .catch(error => console.error('Error:', error));
    }

    // Función para agregar cliente a la lista
    function agregarClienteALista(cliente) {
        const clientesList = document.getElementById('clientes-list');
        const clienteDiv = document.createElement('div');
        clienteDiv.className = 'cliente';
        clienteDiv.dataset.id = cliente.id;
        clienteDiv.innerHTML = `
            <p>Nombre: ${cliente.nombre}</p>
            <p>Correo: ${cliente.correo}</p>
            <p>Dirección: ${cliente.direccion}</p>
            <p>Membresía: ${cliente.membresia}</p>
            <button onclick="editarCliente(${cliente.id})">Editar</button>
            <button onclick="eliminarCliente(${cliente.id})">Eliminar</button>
        `;
        clientesList.appendChild(clienteDiv);
    }

    // Función para actualizar cliente en la lista
    function actualizarClienteEnLista(cliente) {
        const clienteDiv = document.querySelector(`.cliente[data-id="${cliente.id}"]`);
        clienteDiv.innerHTML = `
            <p>Nombre: ${cliente.nombre}</p>
            <p>Correo: ${cliente.correo}</p>
            <p>Dirección: ${cliente.direccion}</p>
            <p>Membresía: ${cliente.membresia}</p>
            <button onclick="editarCliente(${cliente.id})">Editar</button>
            <button onclick="eliminarCliente(${cliente.id})">Eliminar</button>
        `;
    }

    // Función para editar cliente
    window.editarCliente = function(clienteId) {
        currentEditId = clienteId;
        fetch(`/clientes/${clienteId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('edit-nombre').value = data.nombre;
            document.getElementById('edit-correo').value = data.correo;
            document.getElementById('edit-direccion').value = data.direccion;
            document.getElementById('edit-membresia').value = data.membresia;
            editModal.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
    }

    // Función para eliminar cliente
    window.eliminarCliente = function(clienteId) {
        if (confirm('¿Estás seguro de que deseas eliminar este cliente?')) {
            fetch(`/clientes/eliminar/${clienteId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const clienteDiv = document.querySelector(`.cliente[data-id="${clienteId}"]`);
                    clienteDiv.remove();
                } else {
                    alert(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }
});