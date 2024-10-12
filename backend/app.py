from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.exc import SQLAlchemyError
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)
##configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ubasg72abi62gl:pe57b2ca8503d9cbd58763ac4a87e1ae4ea39ae84c8ff769f0e87c490647e3472@c9pv5s2sq0i76o.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddpb2lu396gu31'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app);

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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario_nombre = data.get('usuario_nombre')
    password = data.get('password')

    # Buscar al usuario por su nombre de usuario
    usuario = Usuario.query.filter_by(usuario_nombre=usuario_nombre).first()

    if usuario and bcrypt.check_password_hash(usuario.password, password):
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    else:
        return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401

if __name__ == '__main__':
    app.run(debug=True)