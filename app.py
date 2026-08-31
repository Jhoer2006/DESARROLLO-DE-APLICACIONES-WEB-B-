from flask import Flask, render_template, request, redirect, url_for
from forms import ProductoForm, ClienteForm, ProveedorForm, FacturacionForm
import sqlite3

app = Flask(__name__)

app.config["SECRET_KEY"] = "tecnoweb-clave-secreta"


def conectar_bd():
    conexion = sqlite3.connect("data/ferreteria.db")
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla_productos():

    conexion = conectar_bd()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


def cargar_productos_iniciales():

    productos_iniciales = [
        (
            "Página Web Empresarial",
            "Sitio web profesional y adaptable para empresas y emprendimientos.",
            "Desarrollo"
        ),
        (
            "Tienda Virtual",
            "Solución web para presentar productos y servicios de un negocio en línea.",
            "Comercio Electrónico"
        ),
        (
            "Aplicación Web",
            "Aplicación desarrollada de acuerdo con las necesidades específicas de cada cliente.",
            "Aplicaciones"
        ),
        (
            "Diseño de Interfaces",
            "Diseño de interfaces modernas, organizadas y adaptables a diferentes dispositivos.",
            "Diseño"
        )
    ]

    conexion = conectar_bd()

    for producto in productos_iniciales:

        existe = conexion.execute(
            """
            SELECT id
            FROM productos
            WHERE nombre = ?
            """,
            (producto[0],)
        ).fetchone()

        if existe is None:

            conexion.execute(
                """
                INSERT INTO productos (nombre, descripcion, categoria)
                VALUES (?, ?, ?)
                """,
                producto
            )

    conexion.commit()
    conexion.close()


crear_tabla_productos()
cargar_productos_iniciales()


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route("/")
def inicio():

    empresa = "TecnoWeb"

    descripcion_empresa = (
        "Desarrollo y Soluciones Web para negocios y emprendimientos."
    )

    return render_template(
        "index.html",
        empresa=empresa,
        descripcion_empresa=descripcion_empresa
    )


# ============================================================
# PRODUCTOS / SERVICIOS
# ============================================================

@app.route("/productos", methods=["GET", "POST"])
def productos():

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = conectar_bd()

        conexion.execute(
            """
            INSERT INTO productos (nombre, descripcion, categoria)
            VALUES (?, ?, ?)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.categoria.data
            )
        )

        conexion.commit()
        conexion.close()

        return redirect(url_for("productos"))

    conexion = conectar_bd()

    productos = conexion.execute(
        """
        SELECT
            id,
            nombre,
            descripcion,
            categoria
        FROM productos
        ORDER BY id DESC
        """
    ).fetchall()

    conexion.close()

    return render_template(
        "productos.html",
        productos=productos,
        form=form
    )


# ============================================================
# CLIENTES
# ============================================================

@app.route("/clientes", methods=["GET", "POST"])
def clientes():

    clientes = [
        {
            "nombre": "Amazonía Café",
            "descripcion": (
                "Emprendimiento dedicado a la comercialización "
                "de café y productos derivados."
            ),
            "servicio": "Página Web Empresarial",
            "estado": "Activo"
        },
        {
            "nombre": "Selva Tours",
            "descripcion": (
                "Empresa turística interesada en promocionar "
                "sus servicios mediante una plataforma web."
            ),
            "servicio": "Tienda Virtual",
            "estado": "Activo"
        },
        {
            "nombre": "Puyo Fitness",
            "descripcion": (
                "Centro deportivo que requiere soluciones digitales "
                "para mejorar la gestión de su información."
            ),
            "servicio": "Aplicación Web",
            "estado": "Pendiente"
        }
    ]

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo_cliente = {
            "nombre": form.nombre.data,
            "descripcion": form.descripcion.data,
            "servicio": "Página Web Empresarial",
            "estado": form.estado.data
        }

        clientes.append(nuevo_cliente)

        return redirect(url_for("clientes"))

    return render_template(
        "clientes.html",
        clientes=clientes,
        form=form
    )


# ============================================================
# PROVEEDORES
# ============================================================

@app.route("/proveedores", methods=["GET", "POST"])
def proveedores():

    proveedores = [
        {
            "nombre": "Proveedor de Hosting",
            "descripcion": (
                "Proveedor de servicios de alojamiento para "
                "los sitios web desarrollados por TecnoWeb."
            ),
            "tipo": "Hosting",
            "estado": "Disponible"
        },
        {
            "nombre": "Proveedor de Dominios",
            "descripcion": (
                "Proveedor encargado del registro y administración "
                "de nombres de dominio."
            ),
            "tipo": "Dominios",
            "estado": "Disponible"
        },
        {
            "nombre": "Proveedor de Equipos Tecnológicos",
            "descripcion": (
                "Proveedor de equipos y componentes necesarios "
                "para las actividades de desarrollo."
            ),
            "tipo": "Equipamiento",
            "estado": "Pendiente"
        }
    ]

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo_proveedor = {
            "nombre": form.nombre.data,
            "descripcion": form.descripcion.data,
            "tipo": "Hosting",
            "estado": form.estado.data
        }

        proveedores.append(nuevo_proveedor)

        return redirect(url_for("proveedores"))

    return render_template(
        "proveedores.html",
        proveedores=proveedores,
        form=form
    )


# ============================================================
# FACTURACIÓN
# ============================================================

@app.route("/facturacion", methods=["GET", "POST"])
def facturacion():

    facturas = [
        {
            "numero": "FAC-001",
            "cliente": "Amazonía Café",
            "servicio": "Página Web Empresarial",
            "fecha": "10/08/2026",
            "total": "$150.00",
            "estado": "Pagada"
        },
        {
            "numero": "FAC-002",
            "cliente": "Selva Tours",
            "servicio": "Tienda Virtual",
            "fecha": "11/08/2026",
            "total": "$280.00",
            "estado": "Pendiente"
        },
        {
            "numero": "FAC-003",
            "cliente": "Puyo Fitness",
            "servicio": "Diseño de Interfaces",
            "fecha": "12/08/2026",
            "total": "$95.00",
            "estado": "Pagada"
        }
    ]

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva_factura = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "servicio": form.servicio.data,
            "fecha": form.fecha.data.strftime("%d/%m/%Y"),
            "total": f"${form.total.data:.2f}",
            "estado": form.estado.data
        }

        facturas.append(nueva_factura)

        return redirect(url_for("facturacion"))

    return render_template(
        "facturacion.html",
        facturas=facturas,
        form=form
    )


# ============================================================
# EJECUCIÓN DE LA APLICACIÓN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)