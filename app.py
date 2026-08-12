from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/productos")
def productos():

    productos = [
        {
            "nombre": "Desarrollo Web",
            "descripcion": "Soluciones orientadas al diseño y desarrollo de páginas web utilizando tecnologías actuales.",
            "categoria": "Desarrollo"
        },
        {
            "nombre": "Diseño de Interfaces",
            "descripcion": "Diseño de interfaces web adaptables a diferentes dispositivos mediante HTML5, CSS3 y Bootstrap.",
            "categoria": "Diseño"
        },
        {
            "nombre": "Aplicaciones Web",
            "descripcion": "Aplicaciones web desarrolladas utilizando estructuras organizadas y tecnologías modernas.",
            "categoria": "Aplicaciones"
        }
    ]

    return render_template(
        "productos.html",
        productos=productos
    )


@app.route("/clientes")
def clientes():

    clientes = [
        {
            "nombre": "Cliente 1",
            "descripcion": "Empresa dedicada a la comercialización de productos tecnológicos.",
            "estado": "Activo"
        },
        {
            "nombre": "Cliente 2",
            "descripcion": "Emprendimiento local interesado en soluciones para presencia digital.",
            "estado": "Activo"
        },
        {
            "nombre": "Cliente 3",
            "descripcion": "Negocio que requiere una aplicación web para mejorar la gestión de su información.",
            "estado": "Pendiente"
        }
    ]

    return render_template(
        "clientes.html",
        clientes=clientes
    )


@app.route("/proveedores")
def proveedores():

    proveedores = [
        {
            "nombre": "Proveedor 1",
            "descripcion": "Proveedor de equipos y componentes tecnológicos para proyectos web.",
            "estado": "Disponible"
        },
        {
            "nombre": "Proveedor 2",
            "descripcion": "Empresa encargada de suministrar servicios tecnológicos y digitales.",
            "estado": "Disponible"
        },
        {
            "nombre": "Proveedor 3",
            "descripcion": "Proveedor especializado en recursos necesarios para el desarrollo de aplicaciones.",
            "estado": "Pendiente"
        }
    ]

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


@app.route("/facturacion")
def facturacion():

    facturas = [
        {
            "numero": "FAC-001",
            "cliente": "Cliente 1",
            "fecha": "10/08/2026",
            "total": "$150.00",
            "estado": "Pagada"
        },
        {
            "numero": "FAC-002",
            "cliente": "Cliente 2",
            "fecha": "11/08/2026",
            "total": "$280.00",
            "estado": "Pendiente"
        },
        {
            "numero": "FAC-003",
            "cliente": "Cliente 3",
            "fecha": "12/08/2026",
            "total": "$95.00",
            "estado": "Pagada"
        }
    ]

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


if __name__ == "__main__":
    app.run(debug=True)