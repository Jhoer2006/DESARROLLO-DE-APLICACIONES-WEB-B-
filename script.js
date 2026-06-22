const formulario = document.getElementById("formRegistro");
const lista = document.getElementById("listaRegistros");
const contador = document.getElementById("contador");
const mensaje = document.getElementById("mensaje");

let total = 0;

formulario.addEventListener("submit", function(event) {

    event.preventDefault();

    const nombre = document.getElementById("nombreRegistro").value.trim();
    const descripcion = document.getElementById("descripcionRegistro").value.trim();
    const categoria = document.getElementById("categoriaRegistro").value;

    if (nombre === "" || descripcion === "" || categoria === "") {

        mensaje.innerHTML =
        '<div class="alert alert-danger">Todos los campos son obligatorios.</div>';

        return;
    }

    mensaje.innerHTML =
    '<div class="alert alert-success">Registro agregado correctamente.</div>';

    const columna = document.createElement("div");
    columna.className = "col-md-4 mb-3";

    const tarjeta = document.createElement("div");
    tarjeta.className = "card h-100";

    tarjeta.innerHTML =
    '<div class="card-body">' +
    '<h5 class="card-title">' + nombre + '</h5>' +
    '<p class="card-text">' + descripcion + '</p>' +
    '<p><strong>Categoría:</strong> ' + categoria + '</p>' +
    '<button class="btn btn-danger btnEliminar">Eliminar</button>' +
    '</div>';

    columna.appendChild(tarjeta);
    lista.appendChild(columna);

    total++;
    contador.textContent = total;

    tarjeta.querySelector(".btnEliminar").addEventListener("click", function() {

        columna.remove();

        total--;

        contador.textContent = total;

    });

    formulario.reset();

});