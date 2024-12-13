from flask import Blueprint, request, jsonify
from models import Cliente, Usuario
from extensions import bcrypt, jwt, get_session
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError

from routes import cliente

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario_nombre = data.get('usuario_nombre')
    password = data.get('password')

    with get_session() as session:
        usuario = session.query(Usuario).filter_by(usuario_nombre=usuario_nombre).first()
        if usuario and bcrypt.check_password_hash(usuario.password, password):
            # Cambiar la identidad a id_usuario
            access_token = create_access_token(identity=usuario.id_usuario)
            return jsonify({
                'message': 'Inicio de sesión exitoso',
                'token': access_token,
                'id_usuario': usuario.id_usuario,
                'tipo_usuario': usuario.tipo_usuario
            }), 200
        else:
            return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
@auth_bp.route('/get_cliente', methods=['GET'])
def get_cliente():
    id_usuario = request.args.get('id_usuario', type=int)
    with get_session() as session:
        cliente = session.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if cliente:
            return jsonify({'id_cliente': cliente.id_cliente}), 200
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404
