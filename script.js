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
const btnAgregar = document.getElementById("btnAgregar");
const spinnerAgregar = document.getElementById("spinnerAgregar");
const textoBoton = document.getElementById("textoBoton");

// Elementos del modal de confirmación (Bootstrap)
const modalConfirmarEl = document.getElementById("modalConfirmar");
const modalConfirmar = new bootstrap.Modal(modalConfirmarEl);
const nombreAEliminar = document.getElementById("nombreAEliminar");
const btnConfirmarEliminar = document.getElementById("btnConfirmarEliminar");

let registros = [];
let indiceAEliminar = null;

function validarNombre() {
  const n = nombreCampo.value.trim();
  if (n === "" || n.length < 3) {
    errorNombre.textContent = n === "" ? "El nombre es obligatorio." : "Debe tener mínimo 3 caracteres.";
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
  const d = descripcionCampo.value.trim();
  if (d.length < 10) {
    errorDescripcion.textContent = "La descripción debe tener al menos 10 caracteres.";
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
    errorCategoria.textContent = "Seleccione una categoría.";
    categoriaCampo.classList.add("is-invalid");
    categoriaCampo.classList.remove("is-valid");
    return false;
  }
  errorCategoria.textContent = "";
  categoriaCampo.classList.remove("is-invalid");
  categoriaCampo.classList.add("is-valid");
  return true;
}

nombreCampo.addEventListener("input", validarNombre);
nombreCampo.addEventListener("blur", validarNombre);

descripcionCampo.addEventListener("input", validarDescripcion);
descripcionCampo.addEventListener("blur", validarDescripcion);

categoriaCampo.addEventListener("change", validarCategoria);

function mostrarRegistros() {
  lista.innerHTML = "";
  contador.textContent = registros.length;

  if (registros.length === 0) {
    lista.innerHTML = '<div class="col-12"><div class="alert alert-secondary text-center">No existen registros disponibles.</div></div>';
    return;
  }

  registros.forEach((r, i) => {
    const c = document.createElement("div");
    c.className = "col-md-6 col-lg-4 mb-3";
    c.innerHTML = `
      <div class="card h-100">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title">${r.nombre}</h5>
          <span class="badge bg-success mb-2 align-self-start">${r.categoria}</span>
          <p class="card-text flex-grow-1">${r.descripcion}</p>
          <button class="btn btn-danger btn-sm mt-2 btnEliminar">Eliminar</button>
        </div>
      </div>
    `;
    c.querySelector(".btnEliminar").onclick = () => {
      // En lugar de eliminar directamente, se abre el modal de confirmación
      indiceAEliminar = i;
      nombreAEliminar.textContent = r.nombre;
      modalConfirmar.show();
    };
    lista.appendChild(c);
  });
}

// Confirmación real de la eliminación dentro del modal
btnConfirmarEliminar.addEventListener("click", () => {
  if (indiceAEliminar !== null) {
    registros.splice(indiceAEliminar, 1);
    indiceAEliminar = null;
    mostrarRegistros();
    mensaje.innerHTML = '<div class="alert alert-warning alert-dismissible fade show" role="alert">' +
      'Registro eliminado correctamente.' +
      '<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>';
  }
  modalConfirmar.hide();
});

mostrarRegistros();

formulario.addEventListener("submit", e => {
  e.preventDefault();

  if (!(validarNombre() && validarDescripcion() && validarCategoria())) {
    mensaje.innerHTML = '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
      'Corrija los errores del formulario.' +
      '<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>';
    return;
  }

  // Simulación de proceso/carga usando un spinner de Bootstrap
  btnAgregar.disabled = true;
  spinnerAgregar.classList.remove("d-none");
  textoBoton.textContent = "Guardando...";

  setTimeout(() => {
    registros.push({
      nombre: nombreCampo.value.trim(),
      descripcion: descripcionCampo.value.trim(),
      categoria: categoriaCampo.value
    });

    mensaje.innerHTML = '<div class="alert alert-success alert-dismissible fade show" role="alert">' +
      'Registro agregado correctamente.' +
      '<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>';

    formulario.reset();
    nombreCampo.classList.remove("is-valid");
    descripcionCampo.classList.remove("is-valid");
    categoriaCampo.classList.remove("is-valid");
    mostrarRegistros();

    spinnerAgregar.classList.add("d-none");
    textoBoton.textContent = "Agregar Registro";
    btnAgregar.disabled = false;
  }, 700);
});
