$(document).ready(function() { 
    
    cargarClientes();

    $('#clienteForm').submit(function(e) {
        e.preventDefault();
        var nombre = $('#nombre').val();
        var correo = $('#correo').val();
        var direccion = $('#direccion').val();
        var membresia = $('#membresia').val();

        $.ajax({
            type: 'POST',
            url: '/clientes/agregar/',
            data: {
                nombre: nombre,
                correo: correo,
                direccion: direccion,
                membresia: membresia,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                $('#modalCliente').modal('hide');
                cargarClientes(); 
            }
        });
    });

    function cargarClientes() {
        $.ajax({
            type: 'GET',
            url: '/clientes',  
            success: function(response) {
                
            }
        });
    }
});

