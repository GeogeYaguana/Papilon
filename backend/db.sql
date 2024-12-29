CREATE TYPE tipo_usuario_enum AS ENUM ('local', 'cliente');
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario_nombre VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    tipo_usuario tipo_usuario_enum NOT NULL,
    url_imagen TEXT,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE local (
    id_local SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    nombre_local VARCHAR(150) NOT NULL,
    direccion TEXT NOT NULL,
    cociente_puntos_local NUMERIC(5, 2) DEFAULT 0, 
    descripcion TEXT,
    latitud NUMERIC(9, 6), 
    longitud NUMERIC(9, 6),
    geom GEOGRAPHY(Point, 4326), -- Usamos geografía en lugar de geometría para almacenar coordenadas en formato WGS 84
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    puntos INTEGER DEFAULT 0
);
CREATE TYPE estado_factura_enum AS ENUM ('pendiente', 'pagada', 'anulada', 'reembolsada');

CREATE TABLE factura (
    id_factura SERIAL PRIMARY KEY,
    id_local INTEGER REFERENCES local(id_local) ON DELETE CASCADE,
    id_cliente INTEGER REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    puntos_ganados INTEGER DEFAULT 0,
    estado estado_factura_enum NOT NULL,  
    total NUMERIC(10, 2) NOT NULL
);

--triggers asociados al calculo de los puntos
CREATE OR REPLACE FUNCTION calcular_puntos_ganados()
RETURNS TRIGGER AS $$
BEGIN
    -- Calcular los puntos ganados directamente usando el valor de cociente_puntos_local
    NEW.puntos_ganados := NEW.total * (
        SELECT COALESCE(cociente_puntos_local, 0)
        FROM local
        WHERE id_local = NEW.id_local
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE categoria (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    url_img TEXT
);
CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    id_categoria INTEGER REFERENCES categoria(id_categoria) ON DELETE SET NULL,
    id_local INTEGER REFERENCES local(id_local) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10, 2) NOT NULL,  -- Precio con dos decimales
    puntos_necesario INTEGER,  -- Puede ser NULL, indica productos no canjeables
    foto_url TEXT,
    disponibilidad BOOLEAN DEFAULT TRUE,  -- TRUE indica que el producto está disponible
    descuento NUMERIC(5, 2),  -- Descuento opcional, NULL si no hay descuento
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE detalle_factura (
    id_detalle_factura SERIAL PRIMARY KEY,
    id_factura INTEGER REFERENCES factura(id_factura) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES producto(id_producto) ON DELETE CASCADE,
    precio_unitario NUMERIC(10, 2) NOT NULL,  -- Precio unitario del producto en la factura
    cantidad INTEGER NOT NULL,  -- Cantidad del producto
    subtotal NUMERIC(10, 2) GENERATED ALWAYS AS (precio_unitario * cantidad) STORED,  -- Subtotal calculado automáticamente
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TYPE estado_canje_enum AS ENUM ('pendiente', 'completado', 'cancelado');

CREATE TABLE canje (
    id_canje SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    id_local INTEGER REFERENCES local(id_local) ON DELETE CASCADE,
    estado estado_canje_enum NOT NULL,  -- Definir estado como VARCHAR o ENUM según necesidad
    puntos_utilizados INTEGER NOT NULL,  -- Puntos canjeados por el cliente
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Fecha del canje, con valor predeterminado
);
CREATE TABLE detalle_canje (
    id_detalle_canje SERIAL PRIMARY KEY,
    id_canje INTEGER REFERENCES canje(id_canje) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES producto(id_producto) ON DELETE CASCADE,
    cantidad INTEGER NOT NULL,  -- Cantidad de productos canjeados
    puntos_totales INTEGER NOT NULL,  -- Puntos totales utilizados para este canje
    valor NUMERIC(10, 2) NOT NULL,  -- Valor del producto en el canje
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Fecha de creación del detalle de canje
);


