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

let registros = [];

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
    c.className = "col-md-4 mb-3";
    c.innerHTML = `
      <div class="card h-100">
        <div class="card-body">
          <h5 class="card-title">${r.nombre}</h5>
          <p>${r.descripcion}</p>
          <p><strong>Categoría:</strong> ${r.categoria}</p>
          <button class="btn btn-danger">Eliminar</button>
        </div>
      </div>
    `;
    c.querySelector("button").onclick = () => {
      registros.splice(i, 1);
      mostrarRegistros();
    };
    lista.appendChild(c);
  });
}

mostrarRegistros();

formulario.addEventListener("submit", e => {
  e.preventDefault();

  if (!(validarNombre() && validarDescripcion() && validarCategoria())) {
    mensaje.innerHTML = '<div class="alert alert-danger">Corrija los errores del formulario.</div>';
    return;
  }

  registros.push({
    nombre: nombreCampo.value.trim(),
    descripcion: descripcionCampo.value.trim(),
    categoria: categoriaCampo.value
  });

  mensaje.innerHTML = '<div class="alert alert-success">Registro agregado correctamente.</div>';
  formulario.reset();
  nombreCampo.classList.remove("is-valid");
  descripcionCampo.classList.remove("is-valid");
  categoriaCampo.classList.remove("is-valid");
  mostrarRegistros();
});
