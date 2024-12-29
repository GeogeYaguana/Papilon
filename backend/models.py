from sqlalchemy import Column, Computed, Integer, String, Text, ForeignKey, DateTime, Numeric, Enum
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from extensions import Base
import sqlalchemy as sa

# Enums
tipo_usuario_enum = ENUM('local', 'cliente', name='tipo_usuario_enum', create_type=False)
estado_canje_enum = ENUM('pendiente', 'completado', 'cancelado', name='estado_canje_enum', create_type=False)
estado_factura_enum = ENUM('pendiente', 'pagada', 'anulada', 'reembolsada', name='estado_factura_enum', create_type=False)

# Modelos
class Usuario(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    usuario_nombre = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    tipo_usuario = Column(tipo_usuario_enum, nullable=False)
    url_imagen = Column(Text, nullable=True)
    telefono = Column(String(20), nullable=True)
    fecha_registro = Column(DateTime, default=func.current_timestamp())

    def serialize(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'usuario_nombre': self.usuario_nombre,
            'correo': self.correo,
            'tipo_usuario': self.tipo_usuario,
            'url_imagen': self.url_imagen,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_registro else None
        }

class Local(Base):
    __tablename__ = 'local'

    id_local = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', ondelete='CASCADE'), nullable=False)
    nombre_local = Column(String(150), nullable=False)
    direccion = Column(Text, nullable=False)
    cociente_puntos_local = Column(Numeric(5, 2), default=0)
    descripcion = Column(Text, nullable=True)
    latitud = Column(Numeric(9, 6), nullable=True)
    longitud = Column(Numeric(9, 6), nullable=True)
    geom = Column(Geography('POINT', srid=4326), nullable=True)
    fecha_registro = Column(DateTime, default=func.current_timestamp())

    def serialize(self):
        return {
            'id_local': self.id_local,
            'id_usuario': self.id_usuario,
            'nombre_local': self.nombre_local,
            'direccion': self.direccion,
            'cociente_puntos_local': str(self.cociente_puntos_local),
            'descripcion': self.descripcion,
            'latitud': str(self.latitud),
            'longitud': str(self.longitud),
            'geom': f'POINT({self.latitud} {self.longitud})',
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_registro else None
        }

class Cliente(Base):
    __tablename__ = 'cliente'

    id_cliente = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', ondelete='CASCADE'), nullable=False)
    puntos = Column(Integer, default=0)

    def serialize(self):
        return {
            'id_cliente': self.id_cliente,
            'id_usuario': self.id_usuario,
            'puntos': self.puntos
        }

class Categoria(Base):
    __tablename__ = 'categoria'

    id_categoria = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    url_img = Column(Text, nullable=True)

    def serialize(self):
        return {
            'id_categoria': self.id_categoria,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'url_img': self.url_img
        }

class Producto(Base):
    __tablename__ = 'producto'

    id_producto = Column(Integer, primary_key=True)
    id_categoria = Column(Integer, ForeignKey('categoria.id_categoria', ondelete='SET NULL'), nullable=True)
    id_local = Column(Integer, ForeignKey('local.id_local', ondelete='CASCADE'), nullable=False)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    puntos_necesario = Column(Integer, nullable=True)
    foto_url = Column(Text, nullable=True)
    disponibilidad = Column(sa.Boolean, default=True)
    descuento = Column(Numeric(5, 2), nullable=True)
    fecha_creacion = Column(DateTime, default=func.current_timestamp())

    def serialize(self):
        return {
            'id_producto': self.id_producto,
            'id_categoria': self.id_categoria,
            'id_local': self.id_local,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': str(self.precio),
            'puntos_necesario': self.puntos_necesario,
            'foto_url': self.foto_url,
            'disponibilidad': self.disponibilidad,
            'descuento': str(self.descuento),
            'fecha_creacion': self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_creacion else None
        }

class Canje(Base):
    __tablename__ = 'canje'

    id_canje = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente', ondelete='CASCADE'), nullable=False)
    id_local = Column(Integer, ForeignKey('local.id_local', ondelete='CASCADE'), nullable=False)
    estado = Column(estado_canje_enum, nullable=False)
    puntos_utilizados = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=func.current_timestamp())

    def serialize(self):
        return {
            'id_canje': self.id_canje,
            'id_cliente': self.id_cliente,
            'id_local': self.id_local,
            'estado': self.estado,
            'puntos_utilizados': self.puntos_utilizados,
            'fecha': self.fecha.strftime("%Y-%m-%d %H:%M:%S") if self.fecha else None
        }

class Factura(Base):
    __tablename__ = 'factura'

    id_factura = Column(Integer, primary_key=True, autoincrement=True)
    id_local = Column(Integer, ForeignKey('local.id_local', ondelete='CASCADE'), nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente', ondelete='CASCADE'), nullable=False)
    fecha = Column(DateTime, default=func.current_timestamp())
    puntos_ganados = Column(Integer, default=0, nullable=False)
    estado = Column(estado_factura_enum, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    def serialize(self):
        return {
            'id_factura': self.id_factura,
            'id_local': self.id_local,
            'id_cliente': self.id_cliente,
            'fecha': self.fecha.strftime("%Y-%m-%d %H:%M:%S") if self.fecha else None,
            'puntos_ganados': self.puntos_ganados,
            'estado': self.estado,
            'total': str(self.total)
        }


class DetalleFactura(Base):
    __tablename__ = 'detalle_factura'

    id_detalle_factura = Column(Integer, primary_key=True, autoincrement=True)
    id_factura = Column(Integer, ForeignKey('factura.id_factura', ondelete='CASCADE'), nullable=False)
    id_producto = Column(Integer, ForeignKey('producto.id_producto', ondelete='CASCADE'), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    cantidad = Column(Integer, nullable=False)
    subtotal = Column(
        Numeric(10, 2),
        Computed('precio_unitario * cantidad', persisted=True)  # Declarar subtotal como generado
    )
    fecha_creacion = Column(DateTime, default=func.current_timestamp())

    def serialize(self):
        return {
            'id_detalle_factura': self.id_detalle_factura,
            'id_factura': self.id_factura,
            'id_producto': self.id_producto,
            'precio_unitario': str(self.precio_unitario),
            'cantidad': self.cantidad,
            'subtotal': str(self.subtotal),  # Esto seguirá funcionando porque SQLAlchemy lo calcula
            'fecha_creacion': self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_creacion else None
        }
    

class DetalleCanje(Base):
    __tablename__ = 'detalle_canje'

    id_detalle_canje = Column(Integer, primary_key=True, autoincrement=True)
    id_canje = Column(Integer, ForeignKey('canje.id_canje', ondelete='CASCADE'), nullable=False)
    id_producto = Column(Integer, ForeignKey('producto.id_producto', ondelete='CASCADE'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    puntos_totales = Column(Integer, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    fecha_creacion = Column(DateTime, default=func.current_timestamp())

    # Relaciones
    canje = relationship('Canje', backref='detalles', lazy='joined')
    producto = relationship('Producto', backref='detalles_canje', lazy='joined')

    def serialize(self):
        return {
            'id_detalle_canje': self.id_detalle_canje,
            'id_canje': self.id_canje,
            'id_producto': self.id_producto,
            'cantidad': self.cantidad,
            'puntos_totales': self.puntos_totales,
            'valor': str(self.valor),
            'fecha_creacion': self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_creacion else None
        }
