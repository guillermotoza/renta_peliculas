document.addEventListener('DOMContentLoaded', function() {
    const clientesList = document.getElementById('clientes-list');
    const clienteForm = document.getElementById('cliente-form');
    const editModal = document.getElementById('edit-modal');
    const closeButton = document.querySelector('.close-button');
    const editForm = document.getElementById('edit-form');
    let currentEditId = null;

    // Función para mostrar la sección seleccionada
    window.mostrarSeccion = function(seccionId) {
        const secciones = document.querySelectorAll('.seccion');
        secciones.forEach(seccion => {
            seccion.style.display = 'none';
        });
        document.getElementById(seccionId).style.display = 'block';
    };

    // Mostrar la sección de clientes por defecto
    mostrarSeccion('clientes');

    // Cargar clientes
    function cargarClientes() {
        fetch('/clientes/')
            .then(response => response.json())
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
            });
    }

    cargarClientes();

    // Agregar cliente
    clienteForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(clienteForm);
        fetch('/clientes/agregar/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                cargarClientes();
                clienteForm.reset();
            }
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
                'X-Requested-With': 'XMLHttpRequest'
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

     // Eliminar cliente
     window.eliminarCliente = function(clienteId) {
        if (confirm('¿Estás seguro de que deseas eliminar este cliente?')) {
            fetch(`/clientes/eliminar/${clienteId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
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