from flask import Flask, render_template, redirect, url_for, request
from forms import ProductoForm, ClienteForm, ProveedorForm, FacturacionForm
from conexion.conexion import obtener_conexion

app = Flask(__name__)

app.config["SECRET_KEY"] = "tecnoweb-clave-secreta"


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

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # --------------------------------------------------------
    # Cargar proveedores en el formulario
    # --------------------------------------------------------

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    form.id_proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in proveedores
    ]

    # --------------------------------------------------------
    # AGREGAR PRODUCTO - INSERT
    # --------------------------------------------------------

    if form.validate_on_submit():

        cursor.execute(
            """
            INSERT INTO productos
            (
                nombre,
                descripcion,
                categoria,
                precio,
                stock,
                id_proveedor
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.categoria.data,
                form.precio.data,
                form.stock.data,
                form.id_proveedor.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("productos"))

    # --------------------------------------------------------
    # LISTAR PRODUCTOS - SELECT + JOIN
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.categoria,
            p.precio,
            p.stock,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM productos p
        INNER JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto DESC
        """
    )

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos,
        form=form
    )


# ============================================================
# MODIFICAR PRODUCTO
# ============================================================

@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
def editar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # --------------------------------------------------------
    # BUSCAR PRODUCTO POR ID
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            id_producto,
            nombre,
            descripcion,
            categoria,
            precio,
            stock,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    producto = cursor.fetchone()

    # Si no existe, volver a Productos
    if producto is None:

        cursor.close()
        conexion.close()

        return redirect(url_for("productos"))

    # --------------------------------------------------------
    # CREAR FORMULARIO
    # --------------------------------------------------------

    form = ProductoForm()

    # --------------------------------------------------------
    # CARGAR PROVEEDORES
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
        """
    )

    proveedores = cursor.fetchall()

    form.id_proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in proveedores
    ]

    # --------------------------------------------------------
    # CARGAR DATOS EN EL FORMULARIO
    # --------------------------------------------------------

    if request.method == "GET":

        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]
        form.id_proveedor.data = producto["id_proveedor"]

    # --------------------------------------------------------
    # MODIFICAR PRODUCTO - UPDATE
    # --------------------------------------------------------

    if form.validate_on_submit():

        cursor.execute(
            """
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                categoria = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.categoria.data,
                form.precio.data,
                form.stock.data,
                form.id_proveedor.data,
                id_producto
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("productos"))

    # --------------------------------------------------------
    # LISTAR PRODUCTOS PARA LA VISTA
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.categoria,
            p.precio,
            p.stock,
            pr.nombre AS proveedor
        FROM productos p
        INNER JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto DESC
        """
    )

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos,
        form=form,
        editando=True,
        id_producto=id_producto
    )


# ============================================================
# ELIMINAR PRODUCTO
# ============================================================

@app.route(
    "/productos/eliminar/<int:id_producto>",
    methods=["POST"]
)
def eliminar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # --------------------------------------------------------
    # ELIMINAR PRODUCTO - DELETE
    # --------------------------------------------------------

    cursor.execute(
        """
        DELETE FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("productos"))


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