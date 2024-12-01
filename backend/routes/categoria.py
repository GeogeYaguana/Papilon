# routes/categoria.py

from flask import Blueprint, jsonify, request
from models import Categoria
from extensions import get_session
from sqlalchemy.exc import SQLAlchemyError

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        with get_session() as session:
            categorias = session.query(Categoria).all()
            resultado = [categoria.serialize() for categoria in categorias]
            return jsonify(resultado), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@categoria_bp.route('/categoria', methods=['POST'])
def create_categoria():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    url_img = data.get('url_img')

    if not nombre:
        return jsonify({'error': 'El nombre es obligatorio'}), 400

    nueva_categoria = Categoria(
        nombre=nombre,
        descripcion=descripcion,
        url_img=url_img
    )

    try:
        with get_session() as session:
            session.add(nueva_categoria)
            session.commit()
            return jsonify(nueva_categoria.serialize()), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@categoria_bp.route('/categoria/<int:id_categoria>', methods=['GET'])
def get_categoria(id_categoria):
    try:
        with get_session() as session:
            categoria = session.query(Categoria).get(id_categoria)
            if categoria is None:
                return jsonify({'error': 'Categoría no encontrada'}), 404
            return jsonify(categoria.serialize()), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@categoria_bp.route('/categoria/<int:id_categoria>', methods=['PUT'])
def update_categoria(id_categoria):
    data = request.get_json()
    try:
        with get_session() as session:
            categoria = session.query(Categoria).get(id_categoria)
            if categoria is None:
                return jsonify({'error': 'Categoría no encontrada'}), 404

            categoria.nombre = data.get('nombre', categoria.nombre)
            categoria.descripcion = data.get('descripcion', categoria.descripcion)
            categoria.url_img = data.get('url_img', categoria.url_img)

            session.commit()
            return jsonify(categoria.serialize()), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@categoria_bp.route('/categoria/<int:id_categoria>', methods=['DELETE'])
def delete_categoria(id_categoria):
    try:
        with get_session() as session:
            categoria = session.query(Categoria).get(id_categoria)
            if categoria is None:
                return jsonify({'error': 'Categoría no encontrada'}), 404

            session.delete(categoria)
            session.commit()
            return jsonify({'message': 'Categoría eliminada correctamente'}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
