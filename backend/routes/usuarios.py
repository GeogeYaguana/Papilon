# routes/usuario.py
from flask import Blueprint, request, jsonify
from models import db, Usuario
from extensions import bcrypt
from sqlalchemy.exc import SQLAlchemyError

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuario', methods=['POST'])
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
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@usuario_bp.route('/usuario', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.serialize() for usuario in usuarios])

@usuario_bp.route('/usuario/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(usuario.serialize())

@usuario_bp.route('/usuario/<int:id>', methods=['PUT'])
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
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@usuario_bp.route('/usuario/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado correctamente'})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
