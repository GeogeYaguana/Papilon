# models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from geoalchemy2 import Geography
from extensions import Base

tipo_usuario_enum = ENUM('local', 'cliente', name='tipo_usuario_enum', create_type=False)

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