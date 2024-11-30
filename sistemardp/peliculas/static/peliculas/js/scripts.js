document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const resultadosContainer = document.getElementById('resultados');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const params = new URLSearchParams(formData);

        fetch(`/resultados_pelicula/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                resultadosContainer.innerHTML = '';
                if (data.peliculas.length > 0) {
                    const table = document.createElement('table');
                    table.classList.add('table', 'table-striped');
                    const thead = document.createElement('thead');
                    thead.innerHTML = `
                        <tr>
                            <th>Título</th>
                            <th>Categoría</th>
                            <th>Disponibilidad</th>
                            <th>Precio</th>
                            <th>Calificación</th>
                        </tr>
                    `;
                    table.appendChild(thead);

                    const tbody = document.createElement('tbody');
                    data.peliculas.forEach(pelicula => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${pelicula.titulo}</td>
                            <td>${pelicula.categorias.nombreCatPel}</td>
                            <td>${pelicula.stock}</td>
                            <td>${pelicula.precio_final}</td>
                            <td>${pelicula.calificacion}</td>
                        `;
                        tbody.appendChild(row);
                    });
                    table.appendChild(tbody);
                    resultadosContainer.appendChild(table);
                } else {
                    resultadosContainer.innerHTML = '<p>No se encontraron películas que coincidan con tu búsqueda.</p>';
                }
            })
            .catch(error => console.error('Error:', error));
    });
});