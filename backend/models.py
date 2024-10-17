# models.py
from extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from geoalchemy2 import Geography

tipo_usuario_enum = ENUM('local', 'cliente', name='tipo_usuario_enum', create_type=False)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario_nombre = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    tipo_usuario = db.Column(tipo_usuario_enum, nullable=False)
    url_imagen = db.Column(db.Text, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

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

class Local(db.Model):
    __tablename__ = 'local'
    id_local = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario', ondelete='CASCADE'), nullable=False)
    nombre_local = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    cociente_puntos_local = db.Column(db.Numeric(5, 2), default=0)
    descripcion = db.Column(db.Text, nullable=True)
    latitud = db.Column(db.Numeric(9, 6), nullable=True)
    longitud = db.Column(db.Numeric(9, 6), nullable=True)
    geom = db.Column(Geography('POINT', srid=4326), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

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

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id_cliente = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario', ondelete='CASCADE'), nullable=False)
    puntos = db.Column(db.Integer, default=0)

    def serialize(self):
        return {
            'id_cliente': self.id_cliente,
            'id_usuario': self.id_usuario,
            'puntos': self.puntos
        }
