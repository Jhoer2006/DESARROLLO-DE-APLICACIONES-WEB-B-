const formulario = document.getElementById("formRegistro");

const nombreCampo = document.getElementById("nombreRegistro");
const descripcionCampo = document.getElementById("descripcionRegistro");
const categoriaCampo = document.getElementById("categoriaRegistro");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

const lista = document.getElementById("listaRegistros");
const contador = document.getElementById("contador");
const mensaje = document.getElementById("mensaje");

let total = 0;

function validarNombre() {

const nombre = nombreCampo.value.trim();

if (nombre === "") {
    errorNombre.textContent = "El nombre es obligatorio.";
    nombreCampo.classList.add("is-invalid");
    nombreCampo.classList.remove("is-valid");
    return false;
}

if (nombre.length < 3) {
    errorNombre.textContent = "Debe tener mínimo 3 caracteres.";
    nombreCampo.classList.add("is-invalid");
    nombreCampo.classList.remove("is-valid");
    return false;
}

errorNombre.textContent = "";
nombreCampo.classList.remove("is-invalid");
nombreCampo.classList.add("is-valid");

return true;

}

function validarDescripcion() {

const descripcion = descripcionCampo.value.trim();

if (descripcion.length < 10) {
    errorDescripcion.textContent =
    "La descripción debe tener al menos 10 caracteres.";

    descripcionCampo.classList.add("is-invalid");
    descripcionCampo.classList.remove("is-valid");

    return false;
}

errorDescripcion.textContent = "";

descripcionCampo.classList.remove("is-invalid");
descripcionCampo.classList.add("is-valid");

return true;

}

function validarCategoria() {

if (categoriaCampo.value === "") {

    errorCategoria.textContent =
    "Seleccione una categoría.";

    categoriaCampo.classList.add("is-invalid");
    categoriaCampo.classList.remove("is-valid");

    return false;
}

errorCategoria.textContent = "";

categoriaCampo.classList.remove("is-invalid");
categoriaCampo.classList.add("is-valid");

return true;

}

nombreCampo.addEventListener("blur", validarNombre);
nombreCampo.addEventListener("input", validarNombre);

descripcionCampo.addEventListener("blur", validarDescripcion);
descripcionCampo.addEventListener("input", validarDescripcion);

categoriaCampo.addEventListener("change", validarCategoria);

formulario.addEventListener("submit", function(event) {

event.preventDefault();

const nombreValido = validarNombre();
const descripcionValida = validarDescripcion();
const categoriaValida = validarCategoria();

if (!nombreValido || !descripcionValida || !categoriaValida) {

    mensaje.innerHTML =
    '<div class="alert alert-danger">Corrija los errores del formulario.</div>';

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
'<h5 class="card-title">' + nombreCampo.value + '</h5>' +
'<p class="card-text">' + descripcionCampo.value + '</p>' +
'<p><strong>Categoría:</strong> ' + categoriaCampo.value + '</p>' +
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

nombreCampo.classList.remove("is-valid");
descripcionCampo.classList.remove("is-valid");
categoriaCampo.classList.remove("is-valid");

});
