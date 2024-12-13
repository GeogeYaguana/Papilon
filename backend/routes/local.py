# routes/local.py
from flask import Blueprint, request, jsonify
from models import Local, Usuario
from extensions import get_session
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

local_bp = Blueprint('local_bp', __name__)

@local_bp.route('/locales', methods=['GET'])
@jwt_required()
def get_locales():
    with get_session() as session:
        locales = session.query(Local).all()
        resultado = []

        for local in locales:
            usuario = session.query(Usuario).get(local.id_usuario)
            local_data = local.serialize()
            local_data['usuario'] = {
                'id_usuario': usuario.id_usuario,
                'nombre': usuario.nombre,
                'usuario_nombre': usuario.usuario_nombre,
                'correo': usuario.correo,
                'tipo_usuario': usuario.tipo_usuario
            }
            resultado.append(local_data)

        return jsonify(resultado), 200

@local_bp.route('/locales', methods=['POST'])
@jwt_required()
def create_local():
    data = request.get_json()
    nombre_local = data.get('nombre_local')
    direccion = data.get('direccion')
    cociente_puntos_local = data.get('cociente_puntos_local', 0)
    descripcion = data.get('descripcion')
    latitud = data.get('latitud')
    longitud = data.get('longitud')
    id_usuario = data.get('id_usuario')

    with get_session() as session:
        usuario = session.query(Usuario).get(id_usuario)
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        if usuario.tipo_usuario != 'local':
            return jsonify({'error': 'El usuario no tiene el tipo adecuado para asociarse con un local'}), 403

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
            session.add(nuevo_local)
            session.commit()
            return jsonify(nuevo_local.serialize()), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

@local_bp.route('/locales/<int:local_id>', methods=['PUT'])
@jwt_required()
def update_local(local_id):
    data = request.get_json()

    with get_session() as session:
        local = session.query(Local).get(local_id)
        if local is None:
            return jsonify({'error': 'Local no encontrado'}), 404

        # Opcional: verificar si el usuario tiene permiso para actualizar
        # Por ejemplo, verificar si el usuario actual es el propietario
        # current_user = get_jwt_identity()
        # if local.id_usuario != current_user:
        #     return jsonify({'error': 'No autorizado para actualizar este local'}), 403

        # Actualizar campos si se proporcionan en la solicitud
        nombre_local = data.get('nombre_local')
        direccion = data.get('direccion')
        cociente_puntos_local = data.get('cociente_puntos_local')
        descripcion = data.get('descripcion')
        latitud = data.get('latitud')
        longitud = data.get('longitud')
        id_usuario = data.get('id_usuario')

        if nombre_local is not None:
            local.nombre_local = nombre_local
        if direccion is not None:
            local.direccion = direccion
        if cociente_puntos_local is not None:
            local.cociente_puntos_local = cociente_puntos_local
        if descripcion is not None:
            local.descripcion = descripcion
        if latitud is not None and longitud is not None:
            local.latitud = latitud
            local.longitud = longitud
            local.geom = f'POINT({latitud} {longitud})'
        if id_usuario is not None:
            usuario = session.query(Usuario).get(id_usuario)
            if usuario is None:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            if usuario.tipo_usuario != 'local':
                return jsonify({'error': 'El usuario no tiene el tipo adecuado para asociarse con un local'}), 403
            local.id_usuario = id_usuario

        try:
            session.commit()
            return jsonify(local.serialize()), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

@local_bp.route('/locales/<int:local_id>', methods=['DELETE'])
@jwt_required()
def delete_local(local_id):
    with get_session() as session:
        local = session.query(Local).get(local_id)
        if local is None:
            return jsonify({'error': 'Local no encontrado'}), 404

        # Opcional: verificar si el usuario tiene permiso para eliminar
        # Por ejemplo, verificar si el usuario actual es el propietario
        # current_user = get_jwt_identity()
        # if local.id_usuario != current_user:
        #     return jsonify({'error': 'No autorizado para eliminar este local'}), 403

        try:
            session.delete(local)
            session.commit()
            return jsonify({'message': 'Local eliminado exitosamente'}), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
