CREATE DATABASE IF NOT EXISTS tecnoweb;

USE tecnoweb;

-- Tabla de proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    estado VARCHAR(30) NOT NULL
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    id_proveedor INT NOT NULL,
    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
);

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20),
    telefono VARCHAR(20),
    correo VARCHAR(100),
    descripcion VARCHAR(300),
    estado VARCHAR(30) NOT NULL
);

-- Tabla de facturacion
CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(30) NOT NULL UNIQUE,
    id_cliente INT NOT NULL,
    servicio VARCHAR(150) NOT NULL,
    fecha DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(30) NOT NULL,
    CONSTRAINT fk_factura_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);