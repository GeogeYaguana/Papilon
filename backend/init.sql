-- Insertar datos en la tabla usuario
INSERT INTO usuario (nombre, usuario_nombre, password, correo, tipo_usuario, url_imagen, telefono, fecha_registro)
VALUES 
('Juan Pérez', 'jperez', 'password1', 'jperez@example.com', 'cliente', 'https://example.com/jperez.jpg', '123456789', NOW()),
('Ana López', 'alopez', 'password2', 'alopez@example.com', 'local', 'https://example.com/alopez.jpg', '987654321', NOW());

-- Insertar datos en la tabla cliente (referenciando usuarios)
INSERT INTO cliente (id_usuario, puntos)
VALUES 
(1, 500),  -- cliente relacionado con Juan Pérez
(2, 1000); -- cliente relacionado con Ana López

-- Insertar datos en la tabla local (referenciando usuarios)
INSERT INTO local (id_usuario, nombre_local, direccion, cociente_puntos_local, descripcion, latitud, longitud, geom)
VALUES 
(2, 'Café Central', 'Av. Principal #123', 0.1, 'Cafetería con ambiente acogedor', -2.189595, -79.889582, NULL);

-- Insertar datos en la tabla categoria
INSERT INTO categoria (nombre, descripcion, url_img)
VALUES 
('Tecnología', 'Productos electrónicos y dispositivos', 'https://example.com/tecnologia.jpg'),
('Café', 'Productos y bebidas a base de café', 'https://example.com/cafe.jpg');

-- Insertar datos en la tabla producto (referenciando categorias y locales)
INSERT INTO producto (id_categoria, id_local, nombre, descripcion, precio, puntos_necesario, foto_url, disponibilidad, descuento)
VALUES 
(1, 1, 'Laptop HP', 'Laptop con procesador Intel i7 y 16GB RAM', 1200.00, 1200, 'https://example.com/laptop_hp.jpg', TRUE, 10.00),
(2, 1, 'Café Latte', 'Café con leche espumosa', 3.50, 35, 'https://example.com/cafe_latte.jpg', TRUE, NULL);

-- Insertar datos en la tabla factura (referenciando cliente y local)
INSERT INTO factura (id_cliente, id_local, fecha, puntos_ganados, estado, total)
VALUES 
(1, 1, NOW(), 20, 'pagada', 100.00),
(2, 1, NOW(), 50, 'pendiente', 200.00);

-- Insertar datos en la tabla detalle_factura (referenciando factura y producto)
INSERT INTO detalle_factura (id_factura, id_producto, precio_unitario, cantidad, subtotal)
VALUES 
(1, 1, 1200.00, 1, 1200.00),  -- Laptop HP
(2, 2, 3.50, 2, 7.00);        -- Café Latte

-- Insertar datos en la tabla canje (referenciando cliente y local)
INSERT INTO canje (id_cliente, id_local, estado, puntos_utilizados, fecha)
VALUES 
(1, 1, 'completado', 100, NOW()),
(2, 1, 'pendiente', 50, NOW());

-- Insertar datos en la tabla detalle_canje (referenciando canje y producto)
INSERT INTO detalle_canje (id_canje, id_producto, cantidad, puntos_totales, valor)
VALUES 
(1, 2, 1, 35, 3.50),  -- Canje de un Café Latte
(2, 1, 1, 1200, 1200.00); -- Canje de una Laptop HP
