$(document).ready(function() {
    
    cargarClientes();

    // Manejo del formulario para agregar o editar clientes
    $('#clienteForm').submit(function(e) {
        e.preventDefault();
        var nombre = $('#nombre').val();
        var correo = $('#correo').val();
        var direccion = $('#direccion').val();
        var detallesMembresia = $('#detalles_membresia').val();  // Cambiar a 'detalles_membresia'
    
        $.ajax({
            type: 'POST',
            url: '/clientes/agregar/',
            data: {
                nombre: nombre,
                correo: correo,
                direccion: direccion,
                detalles_membresia: detallesMembresia,  // Cambiar a 'detalles_membresia'
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                $('#modalCliente').modal('hide');
                cargarClientes(); 
            }
        });
    });

    // Cargar los clientes
    function cargarClientes() {
        $.ajax({
            type: 'GET',
            url: '/clientes',  
            success: function(response) {
                var clientes = response.clientes;  // Asegúrate de que esta respuesta esté bien formada
                
                $('#clientesTable tbody').empty();  // Limpiar la tabla antes de llenarla

                // Llenar la tabla con los nuevos datos
                clientes.forEach(function(cliente) {
                    var fila = `<tr>
                        <td>${cliente.nombre}</td>
                        <td>${cliente.correo}</td>
                        <td>${cliente.direccion}</td>
                        <td>${cliente.membresia}</td>
                        <td>
                            <button class="btn btn-warning btn-sm editarClienteBtn" data-id="${cliente.id}">Editar</button>
                            <button class="btn btn-danger btn-sm eliminarClienteBtn" data-id="${cliente.id}">Eliminar</button>
                        </td>
                    </tr>`;
                    $('#clientesTable tbody').append(fila);
                });
            },
            error: function(xhr, status, error) {
                console.error('Error al cargar los clientes: ', status, error);
            }
        });
    }

    // Eliminar cliente
    $(document).on('click', '.eliminarClienteBtn', function() {
        var clienteId = $(this).data('id');
        
        $.ajax({
            type: 'POST',
            url: '/clientes/eliminar/',  
            data: {
                id: clienteId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                cargarClientes();  // Volver a cargar la lista de clientes
            },
            error: function(xhr, status, error) {
                console.error('Error al eliminar cliente: ', status, error);
            }
        });
    });

    // Editar cliente
    $(document).on('click', '.editarClienteBtn', function() {
        var clienteId = $(this).data('id');
        
        $.ajax({
            type: 'GET',
            url: '/clientes/' + clienteId + '/editar/',  
            success: function(response) {
                var cliente = response.cliente;  
                $('#nombre').val(cliente.nombre);
                $('#correo').val(cliente.correo);
                $('#direccion').val(cliente.direccion);
                $('#membresia').val(cliente.membresia);
                
                // Cambiar el título del modal
                $('#modalClienteLabel').text('Editar Cliente');
                
                // Cambiar la acción del formulario
                $('#clienteForm').off('submit').on('submit', function(e) {
                    e.preventDefault();
                    $.ajax({
                        type: 'POST',
                        url: '/clientes/' + clienteId + '/editar/',  
                        data: {
                            nombre: $('#nombre').val(),
                            correo: $('#correo').val(),
                            direccion: $('#direccion').val(),
                            membresia: $('#membresia').val(),
                            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                        },
                        success: function(response) {
                            $('#modalCliente').modal('hide');
                            cargarClientes();  // Volver a cargar la lista de clientes
                        },
                        error: function(xhr, status, error) {
                            console.error('Error al editar cliente: ', status, error);
                        }
                    });
                });
    
                // Mostrar el modal
                $('#modalCliente').modal('show');
            },
            error: function(xhr, status, error) {
                console.error('Error al obtener los datos del cliente: ', status, error);
            }
        });
    });
});
