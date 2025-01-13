from flask import Blueprint, request, jsonify
from models import Cliente, Usuario
from extensions import bcrypt, jwt, get_session
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError
from google.oauth2 import id_token
from google.auth.transport import requests

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
@auth_bp.route('/login_local', methods=['POST'])
def login_local():
    data = request.get_json()
    usuario_nombre = data.get('usuario_nombre')
    password = data.get('password')

    with get_session() as session:
        usuario = session.query(Usuario).filter_by(usuario_nombre=usuario_nombre).first()
        if usuario and bcrypt.check_password_hash(usuario.password, password):
            if usuario.tipo_usuario != 'local':
                return jsonify({'error': 'Acceso restringido a usuarios locales'}), 403  # Forbidden
            access_token = create_access_token(identity=usuario.id_usuario)
            return jsonify({
                'message': 'Inicio de sesión exitoso para usuario local',
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
@auth_bp.route('/login_google', methods=['POST'])
def login_google():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({'error': 'Token de Google es requerido'}), 400

    try:
        # Verificar el token con Google
        client_id = "TU_CLIENT_ID_DE_GOOGLE"
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)

        email = idinfo.get('email')
        nombre = idinfo.get('name')
        picture = idinfo.get('picture')

        with get_session() as session:
            # Verificar si el usuario ya existe
            usuario = session.query(Usuario).filter_by(correo=email).first()

            if not usuario:
                # Crear un nuevo usuario si no existe
                nuevo_usuario = Usuario(
                    usuario_nombre=email.split('@')[0],
                    correo=email,
                    nombre=nombre,
                    tipo_usuario='cliente',  # Tipo de usuario para clientes
                )
                session.add(nuevo_usuario)
                session.commit()

                # Crear un cliente asociado al usuario
                nuevo_cliente = Cliente(
                    id_usuario=nuevo_usuario.id_usuario,
                    puntos=0  # Puntos iniciales para el cliente
                )
                session.add(nuevo_cliente)
                session.commit()

                usuario = nuevo_usuario

            # Generar un token de acceso
            access_token = create_access_token(identity=usuario.id_usuario)

            return jsonify({
                'message': 'Inicio de sesión con Google exitoso',
                'token': access_token,
                'id_usuario': usuario.id_usuario,
                'tipo_usuario': usuario.tipo_usuario
            }), 200

    except ValueError as e:
        return jsonify({'error': 'Token de Google no válido'}), 400

    except SQLAlchemyError as e:
        return jsonify({'error': 'Error de base de datos: ' + str(e)}), 500
