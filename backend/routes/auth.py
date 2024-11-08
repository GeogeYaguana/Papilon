from flask import Blueprint, request, jsonify
from models import Cliente, Usuario
from extensions import bcrypt, jwt, get_session
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario_nombre = data.get('usuario_nombre')
    password = data.get('password')

    with get_session() as session:
        usuario = session.query(Usuario).filter_by(usuario_nombre=usuario_nombre).first()

        if usuario and bcrypt.check_password_hash(usuario.password, password):
            access_token = create_access_token(identity={'usuario_nombre': usuario.usuario_nombre})
            cliente = session.query(Cliente).filter_by(id_usuario=usuario.id_usuario).first()
            usuario_data = usuario.serialize()
            cliente_data = cliente.serialize() if cliente else {}
            return jsonify({'message': 'Inicio de sesión exitoso', 'token': access_token ,'usuario' : usuario_data , 'cliente' :cliente_data}), 200
        else:
            return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401