from flask import Flask, render_template, redirect, url_for, request, flash
from forms import ProductoForm, ClienteForm, ProveedorForm, FacturacionForm
from conexion.conexion import obtener_conexion
from psycopg2.extras import RealDictCursor
from psycopg2 import IntegrityError

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required
)

from models import Usuario

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "tecnoweb-clave-secreta"


# ============================================================
# CONFIGURACIÓN DE FLASK-LOGIN
# ============================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id, usuario FROM usuarios WHERE id = %s",
        (user_id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario:
        return Usuario(usuario[0], usuario[1])

    return None


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route("/", methods=["GET", "POST"])
def inicio():

    empresa = "TecnoWeb"

    producto_id = request.args.get("producto")

    producto_seleccionado = None

    descripcion_empresa = (
        "Desarrollo y Soluciones Web para negocios y emprendimientos."
    )

    # --------------------------------------------------------
    # PRODUCTO SELECCIONADO DESDE EL CATÁLOGO
    # --------------------------------------------------------

    if producto_id:

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT
                id_producto,
                nombre,
                descripcion,
                categoria,
                precio
            FROM productos
            WHERE id_producto = %s
            """,
            (producto_id,)
        )

        producto_seleccionado = cursor.fetchone()

        cursor.close()
        conexion.close()

    # --------------------------------------------------------
    # PROCESAR FORMULARIOS
    # --------------------------------------------------------

    if request.method == "POST":

        tipo_formulario = request.form.get("tipo_formulario")

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # ----------------------------------------------------
        # FORMULARIO DE CONTACTO
        # ----------------------------------------------------

        if tipo_formulario == "contacto":

            nombre = request.form.get("contacto_nombre")
            correo = request.form.get("contacto_correo")
            asunto = request.form.get("contacto_asunto")
            mensaje = request.form.get("contacto_mensaje")

            cursor.execute(
                """
                INSERT INTO mensajes_contacto
                (
                    nombre,
                    correo,
                    asunto,
                    mensaje
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    nombre,
                    correo,
                    asunto,
                    mensaje
                )
            )

            conexion.commit()

            flash(
                "Mensaje enviado con éxito.",
                "success"
            )

            cursor.close()
            conexion.close()

            return redirect(
                url_for("inicio") + "#contacto"
            )

        # ----------------------------------------------------
        # FORMULARIO DE COTIZACIÓN
        # ----------------------------------------------------

        if tipo_formulario == "cotizacion":

            nombre = request.form.get("nombre")
            correo = request.form.get("correo")
            servicio = request.form.get("servicio")
            descripcion = request.form.get("descripcion")

            id_producto = (
                request.form.get("id_producto")
                or None
            )

            # Buscar cliente por correo

            cursor.execute(
                """
                SELECT id_cliente
                FROM clientes
                WHERE correo = %s
                LIMIT 1
                """,
                (correo,)
            )

            cliente = cursor.fetchone()

            # Crear cliente si no existe

            if cliente is None:

                cursor.execute(
                    """
                    INSERT INTO clientes
                    (
                        nombre,
                        correo,
                        estado
                    )
                    VALUES (%s, %s, %s)
                    RETURNING id_cliente
                    """,
                    (
                        nombre,
                        correo,
                        "Activo"
                    )
                )

                id_cliente = cursor.fetchone()[0]

            else:

                id_cliente = cliente[0]

            # Crear solicitud

            cursor.execute(
                """
                INSERT INTO solicitudes
                (
                    nombre,
                    correo,
                    servicio,
                    descripcion,
                    id_producto,
                    id_cliente
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    nombre,
                    correo,
                    servicio,
                    descripcion,
                    id_producto,
                    id_cliente
                )
            )

            conexion.commit()

            cursor.close()
            conexion.close()

            return redirect(
                url_for("inicio") + "#registro"
            )

        cursor.close()
        conexion.close()

        return redirect(
            url_for("inicio")
        )

    # --------------------------------------------------------
    # MOSTRAR PÁGINA PRINCIPAL
    # --------------------------------------------------------

    return render_template(
        "index.html",
        empresa=empresa,
        descripcion_empresa=descripcion_empresa,
        producto_id=producto_id,
        producto_seleccionado=producto_seleccionado
    )


# ============================================================
# REGISTRO DE USUARIO
# ============================================================

@app.route("/crear-cuenta", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Verificar si el usuario ya existe
        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = %s",
            (form.usuario.data,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conexion.close()

            form.usuario.errors.append(
                "El usuario ya existe."
            )

            return render_template(
                "registro.html",
                form=form
            )

        # Generar hash de la contraseña
        password_hash = generate_password_hash(
            form.password.data
        )

        cursor.execute(
            """
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
            """,
            (
                form.usuario.data,
                password_hash
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )


# ============================================================
# INICIO DE SESIÓN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario and check_password_hash(
            usuario[2],
            form.password.data
        ):

            usuario_objeto = Usuario(
                usuario[0],
                usuario[1]
            )

            login_user(usuario_objeto)

            return redirect(url_for("dashboard"))

        form.password.errors.append(
            "Usuario o contraseña incorrectos."
        )

    return render_template(
        "login.html",
        form=form
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    # ==========================================================
    # SOLICITUDES DE COTIZACIÓN
    # ==========================================================

    cursor.execute(
        """
        SELECT
            s.id_solicitud,
            s.nombre,
            s.correo,
            s.servicio,
            s.descripcion,
            s.fecha,
            s.estado,
            p.nombre AS producto,
            c.id_cotizacion,
            c.precio AS precio_cotizacion,
            c.descripcion AS descripcion_cotizacion,
            c.fecha AS fecha_cotizacion,
            c.estado AS estado_cotizacion
        FROM solicitudes s
        LEFT JOIN productos p
            ON s.id_producto = p.id_producto
        LEFT JOIN cotizaciones c
            ON s.id_solicitud = c.id_solicitud
        ORDER BY s.id_solicitud ASC
        """
    )

    solicitudes = cursor.fetchall()

    # ==========================================================
    # MENSAJES DE CONTACTO
    # ==========================================================

    cursor.execute(
        """
        SELECT
            id_mensaje,
            nombre,
            correo,
            asunto,
            mensaje,
            fecha,
            estado
        FROM mensajes_contacto
        ORDER BY fecha DESC
        """
    )

    mensajes_contacto = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "dashboard.html",
        solicitudes=solicitudes,
        mensajes_contacto=mensajes_contacto
    )


@app.route("/cotizacion/<int:id_solicitud>", methods=["POST"])
@login_required
def crear_cotizacion(id_solicitud):

    precio = request.form.get("precio")
    descripcion = request.form.get("descripcion")

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO cotizaciones
        (id_solicitud, precio, descripcion)
        VALUES (%s, %s, %s)
        """,
        (id_solicitud, precio, descripcion)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("dashboard"))


@app.route("/solicitud/<int:id_solicitud>/estado", methods=["POST"])
@login_required
def cambiar_estado_solicitud(id_solicitud):

    nuevo_estado = request.form.get("estado")

    estados_permitidos = [
        "Pendiente",
        "En revisión",
        "Cotizada",
        "Aceptada",
        "En desarrollo",
        "Finalizada"
    ]

    if nuevo_estado not in estados_permitidos:
        return redirect(url_for("dashboard"))

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE solicitudes
        SET estado = %s
        WHERE id_solicitud = %s
        """,
        (nuevo_estado, id_solicitud)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("dashboard"))


@app.route("/cotizacion/<int:id_cotizacion>/estado", methods=["POST"])
@login_required
def cambiar_estado_cotizacion(id_cotizacion):

    nuevo_estado = request.form.get("estado")

    estados_permitidos = [
        "Pendiente",
        "Aceptada",
        "Rechazada"
    ]

    if nuevo_estado not in estados_permitidos:
        return redirect(url_for("dashboard"))

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE cotizaciones
        SET estado = %s
        WHERE id_cotizacion = %s
        """,
        (nuevo_estado, id_cotizacion)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("dashboard"))


@app.route("/cotizacion/<int:id_cotizacion>/factura", methods=["POST"])
@login_required
def crear_factura(id_cotizacion):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Buscar la cotización y la solicitud relacionada
    cursor.execute(
        """
        SELECT
            c.precio,
            c.estado,
            s.id_solicitud,
            s.id_cliente,
            s.nombre,
            s.correo,
            s.servicio
        FROM cotizaciones c
        INNER JOIN solicitudes s
            ON c.id_solicitud = s.id_solicitud
        WHERE c.id_cotizacion = %s
        """,
        (id_cotizacion,)
    )

    datos = cursor.fetchone()

    # Si la cotización no existe, volver al panel
    if datos is None:

        cursor.close()
        conexion.close()

        return redirect(url_for("dashboard"))

    precio = datos[0]
    estado_cotizacion = datos[1]
    id_solicitud = datos[2]
    id_cliente = datos[3]
    nombre = datos[4]
    correo = datos[5]
    servicio = datos[6]

    # La factura solamente puede generarse
    # cuando la cotización está aceptada
    if estado_cotizacion != "Aceptada":

        cursor.close()
        conexion.close()

        return redirect(url_for("dashboard"))

    # Comprobar si ya existe una factura para esta cotización
    cursor.execute(
        """
        SELECT id_factura
        FROM facturas
        WHERE id_cotizacion = %s
        """,
        (id_cotizacion,)
    )

    factura_existente = cursor.fetchone()

    if factura_existente is not None:

        cursor.close()
        conexion.close()

        return redirect(url_for("facturacion"))

    # Si la solicitud todavía no tiene cliente,
    # crear el cliente automáticamente
    if id_cliente is None:

        cursor.execute(
            """
            SELECT id_cliente
            FROM clientes
            WHERE correo = %s
            LIMIT 1
            """,
            (correo,)
        )

        cliente_existente = cursor.fetchone()

        if cliente_existente is not None:

            id_cliente = cliente_existente[0]

        else:

            cursor.execute(
                """
                INSERT INTO clientes
                (nombre, correo, estado)
                VALUES (%s, %s, %s)
                RETURNING id_cliente
                """,
                (
                    nombre,
                    correo,
                    "Activo"
                )
            )

            id_cliente = cursor.fetchone()[0]

        # Asociar el cliente con la solicitud
        cursor.execute(
            """
            UPDATE solicitudes
            SET id_cliente = %s
            WHERE id_solicitud = %s
            """,
            (
                id_cliente,
                id_solicitud
            )
        )

    # Generar número de factura
    numero_factura = f"FAC-{id_cotizacion:03d}"

    # Crear factura
    cursor.execute(
        """
        INSERT INTO facturas
        (
            numero,
            id_cliente,
            servicio,
            fecha,
            total,
            estado,
            id_cotizacion
        )
        VALUES
        (
            %s,
            %s,
            %s,
            CURRENT_DATE,
            %s,
            %s,
            %s
        )
        """,
        (
            numero_factura,
            id_cliente,
            servicio,
            precio,
            "Pendiente",
            id_cotizacion
        )
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("facturacion"))


# ============================================================
# CERRAR SESIÓN
# ============================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# ============================================================
# PRODUCTOS / SERVICIOS
# ============================================================

@app.route("/productos", methods=["GET", "POST"])
def productos():

    form = ProductoForm()

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

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
        (
            proveedor["id_proveedor"],
            proveedor["nombre"]
        )
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
@login_required
def editar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

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
        (
            proveedor["id_proveedor"],
            proveedor["nombre"]
        )
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
@login_required
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
@login_required
def clientes():

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    form = ClienteForm()

    if form.validate_on_submit():

        cursor.execute(
            """
            INSERT INTO clientes
            (
                nombre,
                descripcion,
                estado
            )
            VALUES (%s, %s, %s)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.estado.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("clientes"))

    cursor.execute(
        """
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo,
            descripcion,
            estado
        FROM clientes
        ORDER BY id_cliente
        """
    )

    clientes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "clientes.html",
        clientes=clientes,
        form=form
    )


# ============================================================
# PROVEEDORES
# ============================================================

@app.route("/proveedores", methods=["GET", "POST"])
@login_required
def proveedores():

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    form = ProveedorForm()

    if form.validate_on_submit():

        cursor.execute(
            """
            INSERT INTO proveedores
            (
                nombre,
                descripcion,
                estado
            )
            VALUES (%s, %s, %s)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.estado.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("proveedores"))

    cursor.execute(
        """
        SELECT
            id_proveedor,
            nombre,
            descripcion,
            estado
        FROM proveedores
        ORDER BY id_proveedor
        """
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores,
        form=form
    )
@app.route("/proveedor/<int:id_proveedor>/eliminar", methods=["POST"])
@login_required
def eliminar_proveedor(id_proveedor):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM proveedores
            WHERE id_proveedor = %s
            """,
            (id_proveedor,)
        )

        conexion.commit()

    except IntegrityError:

        conexion.rollback()

        flash(
            "No se puede eliminar este proveedor porque tiene productos asociados.",
            "danger"
        )

    finally:

        cursor.close()
        conexion.close()

    return redirect(url_for("proveedores"))


# ============================================================
# FACTURACIÓN
# ============================================================

@app.route("/facturacion", methods=["GET"])
@login_required
def facturacion():

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            f.id_factura,
            f.numero,
            c.nombre AS cliente,
            f.servicio,
            f.fecha,
            f.total,
            f.estado,
            f.id_cotizacion,
            co.precio AS precio_cotizacion,
            co.estado AS estado_cotizacion
        FROM facturas f
        LEFT JOIN clientes c
            ON f.id_cliente = c.id_cliente
        LEFT JOIN cotizaciones co
            ON f.id_cotizacion = co.id_cotizacion
       ORDER BY f.numero ASC
        """
    )

    facturas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


# ============================================================
# EJECUCIÓN DE LA APLICACIÓN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)