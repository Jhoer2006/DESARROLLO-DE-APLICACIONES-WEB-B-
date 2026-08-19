from flask import Flask, render_template

app = Flask(__name__)


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

@app.route("/productos")
def productos():

    productos = [
        {
            "nombre": "Página Web Empresarial",
            "descripcion": (
                "Sitio web profesional y adaptable para empresas "
                "y emprendimientos."
            ),
            "categoria": "Desarrollo Web",
            "precio": "$150.00",
            "estado": "Disponible"
        },
        {
            "nombre": "Tienda Virtual",
            "descripcion": (
                "Solución web para presentar productos y servicios "
                "de un negocio en línea."
            ),
            "categoria": "Comercio Electrónico",
            "precio": "$280.00",
            "estado": "Disponible"
        },
        {
            "nombre": "Aplicación Web",
            "descripcion": (
                "Aplicación desarrollada de acuerdo con las "
                "necesidades específicas de cada cliente."
            ),
            "categoria": "Aplicaciones",
            "precio": "$500.00",
            "estado": "Disponible"
        },
        {
            "nombre": "Diseño de Interfaces",
            "descripcion": (
                "Diseño de interfaces modernas, organizadas y "
                "adaptables a diferentes dispositivos."
            ),
            "categoria": "Diseño",
            "precio": "$95.00",
            "estado": "Disponible"
        }
    ]

    return render_template(
        "productos.html",
        productos=productos
    )


# ============================================================
# CLIENTES
# ============================================================

@app.route("/clientes")
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

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# ============================================================
# PROVEEDORES
# ============================================================

@app.route("/proveedores")
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

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# ============================================================
# FACTURACIÓN
# ============================================================

@app.route("/facturacion")
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

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


# ============================================================
# EJECUCIÓN DE LA APLICACIÓN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)