# routes/cliente.py
from flask import Blueprint, request, jsonify
from models import Cliente, Usuario
from extensions import bcrypt, get_session
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity

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
            session.flush()  # Para obtener el id_usuario antes de crear Cliente
            nuevo_cliente = Cliente(
                id_usuario=nuevo_usuario.id_usuario,
                puntos=puntos
            )
            session.add(nuevo_cliente)
            session.commit()
            return jsonify({
                'mensaje': 'Usuario y cliente creados correctamente',
                'id_usuario': nuevo_usuario.id_usuario,
                'id_cliente': nuevo_cliente.id_cliente
            }), 201
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400

@cliente_bp.route('/clientes', methods=['GET'])
@jwt_required()
def get_clientes():
    with get_session() as session:
        clientes = session.query(Cliente).all()
        resultado = []

        for cliente in clientes:
            usuario = session.query(Usuario).get(cliente.id_usuario)
            if usuario:
                cliente_data = cliente.serialize()
                cliente_data['usuario'] = {
                    'id_usuario': usuario.id_usuario,
                    'nombre': usuario.nombre,
                    'usuario_nombre': usuario.usuario_nombre,
                    'correo': usuario.correo,
                    'tipo_usuario': usuario.tipo_usuario,
                    'url_imagen': usuario.url_imagen,
                    'telefono': usuario.telefono
                }
                resultado.append(cliente_data)

        return jsonify(resultado), 200

@cliente_bp.route('/clientes/<int:id_cliente>', methods=['GET'])
@jwt_required()
def get_cliente(id_cliente):
    with get_session() as session:
        cliente = session.query(Cliente).get(id_cliente)
        if cliente is None:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        usuario = session.query(Usuario).get(cliente.id_usuario)
        if not usuario:
            return jsonify({'error': 'Usuario asociado no encontrado'}), 404

        cliente_data = cliente.serialize()
        cliente_data['usuario'] = {
            'id_usuario': usuario.id_usuario,
            'nombre': usuario.nombre,
            'usuario_nombre': usuario.usuario_nombre,
            'correo': usuario.correo,
            'tipo_usuario': usuario.tipo_usuario,
            'url_imagen': usuario.url_imagen,
            'telefono': usuario.telefono,
            'puntos':cliente.puntos,
        }

        return jsonify(cliente_data), 200

@cliente_bp.route('/clientes/<int:id_cliente>', methods=['PUT'])
@jwt_required()
def update_cliente(id_cliente):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    with get_session() as session:
        cliente = session.query(Cliente).get(id_cliente)
        if cliente is None:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        usuario = session.query(Usuario).get(cliente.id_usuario)
        if not usuario:
            return jsonify({'error': 'Usuario asociado no encontrado'}), 404

        # Verificar si el usuario actual es el propietario del cliente o tiene permisos
        if usuario.id_usuario != current_user_id:
            return jsonify({'error': 'No autorizado para actualizar este cliente'}), 403

        # Actualizar campos del Usuario
        nombre = data.get('nombre')
        usuario_nombre = data.get('usuario_nombre')
        password = data.get('password')
        correo = data.get('correo')
        url_imagen = data.get('url_imagen')
        telefono = data.get('telefono')

        if nombre is not None:
            usuario.nombre = nombre
        if usuario_nombre is not None:
            # Verificar si el nuevo nombre de usuario ya está en uso
            usuario_existente = session.query(Usuario).filter_by(usuario_nombre=usuario_nombre).first()
            if usuario_existente and usuario_existente.id_usuario != usuario.id_usuario:
                return jsonify({'error': 'El nombre de usuario ya está en uso'}), 400
            usuario.usuario_nombre = usuario_nombre
        if password is not None:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            usuario.password = hashed_password
        if correo is not None:
            usuario.correo = correo
        if url_imagen is not None:
            usuario.url_imagen = url_imagen
        if telefono is not None:
            usuario.telefono = telefono

        # Actualizar campos del Cliente
        puntos = data.get('puntos')
        if puntos is not None:
            cliente.puntos = puntos

        try:
            session.commit()
            return jsonify({
                'mensaje': 'Cliente actualizado correctamente',
                'id_cliente': cliente.id_cliente,
                'id_usuario': usuario.id_usuario
            }), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

@cliente_bp.route('/clientes/<int:id_cliente>', methods=['DELETE'])
@jwt_required()
def delete_cliente(id_cliente):
    current_user_id = get_jwt_identity()

    with get_session() as session:
        cliente = session.query(Cliente).get(id_cliente)
        if cliente is None:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        usuario = session.query(Usuario).get(cliente.id_usuario)
        if not usuario:
            return jsonify({'error': 'Usuario asociado no encontrado'}), 404

        # Verificar si el usuario actual es el propietario del cliente o tiene permisos
        if usuario.id_usuario != current_user_id:
            return jsonify({'error': 'No autorizado para eliminar este cliente'}), 403

        try:
            session.delete(cliente)
            session.delete(usuario)
            session.commit()
            return jsonify({'mensaje': 'Cliente y usuario eliminados exitosamente'}), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
@cliente_bp.route('/cliente_id/<int:id_usuario>', methods=['GET'])
@jwt_required()
def get_cliente_id_by_usuario_id(id_usuario):
    with get_session() as session:
        # Buscar al cliente relacionado con el id_usuario
        cliente = session.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if cliente is None:
            return jsonify({'error': 'Cliente no encontrado para el usuario proporcionado'}), 404
        
        return jsonify({'id_cliente': cliente.id_cliente}), 200
@cliente_bp.route('/clientes/<int:id_cliente>/nombre', methods=['GET'])
@jwt_required()
def get_cliente_nombre(id_cliente):
    with get_session() as session:
        # Buscar al cliente por su ID
        cliente = session.query(Cliente).get(id_cliente)
        if cliente is None:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        # Buscar el usuario asociado al cliente
        usuario = session.query(Usuario).get(cliente.id_usuario)
        if not usuario:
            return jsonify({'error': 'Usuario asociado no encontrado'}), 404

        # Retornar el nombre del cliente
        return jsonify({'nombre': usuario.nombre}), 200
