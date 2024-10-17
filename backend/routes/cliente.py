# routes/cliente.py
from flask import Blueprint, request, jsonify
from models import Cliente, Usuario
from extensions import bcrypt, get_session
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/crear_cliente', methods=['POST'])
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
        with get_session() as session:
            usuario_existente = session.query(Usuario).filter_by(usuario_nombre=usuario_nombre).first()
            if usuario_existente:
                return jsonify({'error': 'El nombre de usuario ya está en uso'}), 400

            session.add(nuevo_usuario)
            session.flush()
            nuevo_cliente = Cliente(
                id_usuario=nuevo_usuario.id_usuario,
                puntos=puntos
            )
            session.add(nuevo_cliente)
            session.commit()
            return jsonify({
                'mensaje': 'Usuario y cliente creados correctamente',
                'id_usuario': nuevo_usuario.id_usuario
            }), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@cliente_bp.route('/clientes', methods=['GET'])
def get_clientes():
    with get_session() as session:
        clientes = session.query(Cliente).all()
        resultado = []

        for cliente in clientes:
            usuario = session.query(Usuario).get(cliente.id_usuario)
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

@cliente_bp.route('/clientes/<int:id_cliente>', methods=['GET'])
@jwt_required()
def get_cliente(id_cliente):
    with get_session() as session:
        cliente = session.query(Cliente).get(id_cliente)
        if cliente is None:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        usuario = session.query(Usuario).get(cliente.id_usuario)
        cliente_data = cliente.serialize()
        cliente_data['usuario'] = {
            'id_usuario': usuario.id_usuario,
            'nombre': usuario.nombre,
            'usuario_nombre': usuario.usuario_nombre,
            'correo': usuario.correo,
            'tipo_usuario': usuario.tipo_usuario
        }

        return jsonify(cliente_data)
