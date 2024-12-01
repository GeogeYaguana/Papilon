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

        return jsonify(resultado)

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
