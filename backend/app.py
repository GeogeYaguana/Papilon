from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS  # Importar la extensión CORS
from flask_bcrypt import Bcrypt
from geoalchemy2 import Geography
from sqlalchemy import text
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash  # Asegúrate de usar werkzeug si usas hashing
from datetime import timedelta
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token
import os
import socket

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8081"}})
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Cargar la clave secreta desde .env
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
jwt = JWTManager(app)

##configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ubasg72abi62gl:pe57b2ca8503d9cbd58763ac4a87e1ae4ea39ae84c8ff769f0e87c490647e3472@c9pv5s2sq0i76o.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddpb2lu396gu31'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app);

def get_local_ip():
    """Obtiene la dirección IP local de la máquina."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

## defino el modelo que va a parametrizar la tabla en un objeto
tipo_usuario_enum = ENUM('local', 'cliente', name='tipo_usuario_enum', create_type=False)
class Usuario(db.Model):
    __tablename__='usuario'
    id_usuario = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario_nombre = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    tipo_usuario = db.Column(tipo_usuario_enum, nullable=False)
    url_imagen = db.Column(db.Text, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
    ## serializo para volverlo un json
    def serialize(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'usuario_nombre': self.usuario_nombre,
            'correo': self.correo,
            'tipo_usuario': self.tipo_usuario,
            'url_imagen': self.url_imagen,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")
        }

## defino las rutas

@app.route('/usuario', methods=['POST'])
def create_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    usuario_nombre = data.get('usuario_nombre')
    password = data.get('password')
    correo = data.get('correo')
    tipo_usuario = data.get('tipo_usuario')
    url_imagen = data.get('url_imagen')
    telefono = data.get('telefono')
    usuario_existente = Usuario.query.filter_by(usuario_nombre=usuario_nombre).first()
    if usuario_existente:
        return jsonify({'error': 'El nombre de usuario ya está en uso'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    nuevo_usuario = Usuario(
        nombre=nombre,
        usuario_nombre=usuario_nombre,
        password=hashed_password,
        correo=correo,
        tipo_usuario=tipo_usuario,
        url_imagen=url_imagen,
        telefono=telefono
    )
    
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(nuevo_usuario.serialize()), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

# Leer todos los usuarios (GET)
@app.route('/usuario', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.serialize() for usuario in usuarios])

# Leer un usuario por ID (GET)
@app.route('/usuario/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(usuario.serialize())

# Actualizar un usuario (PUT)
@app.route('/usuario/<int:id>', methods=['PUT'])
def update_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()
    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.usuario_nombre = data.get('usuario_nombre', usuario.usuario_nombre)
    usuario.password = data.get('password', usuario.password)
    usuario.correo = data.get('correo', usuario.correo)
    usuario.tipo_usuario = data.get('tipo_usuario', usuario.tipo_usuario)
    usuario.url_imagen = data.get('url_imagen', usuario.url_imagen)
    usuario.telefono = data.get('telefono', usuario.telefono)

    try:
        db.session.commit()
        return jsonify(usuario.serialize())
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

# Eliminar un usuario (DELETE)
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado correctamente'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

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
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")
        }
@app.route('/locales', methods=['GET'])
def get_locales():
    with Session(db.engine) as session:
        locales = session.query(Local).all()  # Obtener todos los locales
        resultado = []

        for local in locales:
            usuario = session.get(Usuario, local.id_usuario)  # Usar Session.get() en lugar de query.get()
            local_data = local.serialize()  # Asumimos que Local tiene un método serialize
            local_data['usuario'] = {
                'id_usuario': usuario.id_usuario,
                'nombre': usuario.nombre,
                'usuario_nombre': usuario.usuario_nombre,
                'correo': usuario.correo,
                'tipo_usuario': usuario.tipo_usuario
            }
            resultado.append(local_data)

    return jsonify(resultado)


@app.route('/locales', methods=['POST'])
def create_local():
    data = request.get_json()
    nombre_local = data.get('nombre_local')
    direccion = data.get('direccion')
    cociente_puntos_local = data.get('cociente_puntos_local', 0)
    descripcion = data.get('descripcion')
    latitud = data.get('latitud')
    longitud = data.get('longitud')
    id_usuario = data.get('id_usuario')

    # Verificar que el usuario existe y es del tipo 'local'
    usuario = Usuario.query.get(id_usuario)
    
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    if usuario.tipo_usuario != 'local':
        return jsonify({'error': 'El usuario no tiene el tipo adecuado para asociarse con un local'}), 403

    # Crear el nuevo local solo si el usuario es válido
    nuevo_local = Local(
        nombre_local=nombre_local,
        direccion=direccion,
        cociente_puntos_local=cociente_puntos_local,
        descripcion=descripcion,
        latitud=latitud,
        longitud=longitud,
        geom=f'POINT({latitud} {longitud})',
        id_usuario=id_usuario
    )
    
    try:
        db.session.add(nuevo_local)
        db.session.commit()
        return jsonify(nuevo_local.serialize()), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400


# Modelo para la tabla 'Cliente'
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

@app.route('/crear_cliente', methods=['POST'])
def create_usuario_y_cliente():
    data = request.get_json()
    nombre = data.get('nombre')
    usuario_nombre = data.get('usuario_nombre')
    password = data.get('password')
    correo = data.get('correo')
    tipo_usuario = data.get('tipo_usuario')  # Debe ser 'cliente'
    url_imagen = data.get('url_imagen')
    telefono = data.get('telefono')
    puntos = data.get('puntos', 0)

    if tipo_usuario != 'cliente':
        return jsonify({'error': 'El tipo de usuario debe ser cliente para crear un cliente'}), 400

    try:
        # Crear una nueva sesión explícita
        with Session(db.engine) as session:
            # Iniciar una transacción explícita dentro de la sesión
            with session.begin():
                # Crear el usuario con SQL personalizado
                sql_usuario = text("""
                    INSERT INTO usuario (nombre, usuario_nombre, password, correo, tipo_usuario, url_imagen, telefono)
                    VALUES (:nombre, :usuario_nombre, :password, :correo, :tipo_usuario, :url_imagen, :telefono)
                    RETURNING id_usuario
                """)
                result = session.execute(sql_usuario, {
                    'nombre': nombre,
                    'usuario_nombre': usuario_nombre,
                    'password': password,
                    'correo': correo,
                    'tipo_usuario': tipo_usuario,
                    'url_imagen': url_imagen,
                    'telefono': telefono
                })

                # Obtener el ID del nuevo usuario creado
                id_usuario = result.fetchone()[0]

                # Crear el cliente asociado al usuario
                sql_cliente = text("""
                    INSERT INTO cliente (id_usuario, puntos)
                    VALUES (:id_usuario, :puntos)
                """)
                session.execute(sql_cliente, {
                    'id_usuario': id_usuario,
                    'puntos': puntos
                })

            # Confirmar la transacción (session.commit() es implícito en el bloque begin)
            return jsonify({
                'mensaje': 'Usuario y cliente creados correctamente',
                'id_usuario': id_usuario
            }), 201

    except SQLAlchemyError as e:
        # No es necesario un rollback explícito dentro de session.begin(), ya que se hace automáticamente
        return jsonify({'error': str(e)}), 400

    
@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    resultado = []

    for cliente in clientes:
        usuario = Usuario.query.get(cliente.id_usuario)
        cliente_data = cliente.serialize()
        cliente_data['usuario'] = {
            'id_usuario': usuario.id_usuario,
            'nombre': usuario.nombre,
            'usuario_nombre': usuario.usuario_nombre,
            'correo': usuario.correo,
            'tipo_usuario': usuario.tipo_usuario
        }
        resultado.append(cliente_data)

    return jsonify(resultado)
@app.route('/clientes/<int:id_cliente>', methods=['GET'])
@jwt_required()  # Añadir este decorador para proteger la ruta
def get_cliente(id_cliente):
    with Session(db.engine) as session:
        cliente = session.get(Cliente, id_cliente)
        
        if cliente is None:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        usuario = session.get(Usuario, cliente.id_usuario)
        cliente_data = cliente.serialize()
        cliente_data['usuario'] = {
            'id_usuario': usuario.id_usuario,
            'nombre': usuario.nombre,
            'usuario_nombre': usuario.usuario_nombre,
            'correo': usuario.correo,
            'tipo_usuario': usuario.tipo_usuario
        }

        return jsonify(cliente_data)
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario_nombre = data.get('usuario_nombre')
    password = data.get('password')

    # Buscar al usuario por su nombre de usuario
    usuario = Usuario.query.filter_by(usuario_nombre=usuario_nombre).first()

    if usuario and bcrypt.check_password_hash(usuario.password, password):
        # Crear un token JWT para el usuario
        access_token = create_access_token(identity={'usuario_nombre': usuario.usuario_nombre})
        return jsonify({'message': 'Inicio de sesión exitoso', 'token': access_token}), 200
    else:
        return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401



if __name__ == '__main__':
    # Obtiene la IP local
    local_ip = get_local_ip()
    
    print(f" * La aplicación Flask está disponible en:\n")
    print(f" * Local:      http://127.0.0.1:5000")
    print(f" * Red local:  http://{local_ip}:5000\n")
    
    # Ejecuta Flask en todas las interfaces de red
    app.run(host='0.0.0.0', port=5000,debug=True)