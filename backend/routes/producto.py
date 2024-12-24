# routes/producto.py

from flask import Blueprint, jsonify, request
from extensions import get_session
from models import Producto, Categoria, Local
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

producto_bp = Blueprint('producto_bp', __name__)

# Ruta para obtener todos los productos
@producto_bp.route('/productos', methods=['GET'])
@jwt_required()
def get_productos():
    try:
        with get_session() as session:
            productos = session.query(Producto).all()
            resultado = [producto.serialize() for producto in productos]
            return jsonify(resultado), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener un producto específico por ID
@producto_bp.route('/producto/<int:id_producto>', methods=['GET'])
@jwt_required()
def get_producto(id_producto):
    try:
        with get_session() as session:
            producto = session.query(Producto).get(id_producto)
            if producto is None:
                return jsonify({'error': 'Producto no encontrado'}), 404
            return jsonify(producto.serialize()), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear un nuevo producto
@producto_bp.route('/producto', methods=['POST'])
@jwt_required()
def create_producto():
    data = request.get_json()
    
    # Obtener y validar los datos necesarios
    id_categoria = data.get('id_categoria')
    id_local = data.get('id_local')
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    puntos_necesario = data.get('puntos_necesario')
    foto_url = data.get('foto_url')
    disponibilidad = data.get('disponibilidad', True)
    descuento = data.get('descuento')
    
    # Validaciones básicas
    if not nombre or not precio or not id_local:
        return jsonify({'error': 'Nombre, precio e id_local son campos obligatorios'}), 400
    
    try:
        with get_session() as session:
            # Verificar que el local existe
            local = session.query(Local).get(id_local)
            if local is None:
                return jsonify({'error': 'Local no encontrado'}), 404
            
            # Si se proporciona id_categoria, verificar que exista
            categoria = None
            if id_categoria:
                categoria = session.query(Categoria).get(id_categoria)
                if categoria is None:
                    return jsonify({'error': 'Categoría no encontrada'}), 404
            
            # Crear el nuevo producto
            nuevo_producto = Producto(
                id_categoria=id_categoria,
                id_local=id_local,
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                puntos_necesario=puntos_necesario,
                foto_url=foto_url,
                disponibilidad=disponibilidad,
                descuento=descuento
            )
            
            session.add(nuevo_producto)
            session.commit()
            return jsonify(nuevo_producto.serialize()), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar un producto existente
@producto_bp.route('/producto/<int:id_producto>', methods=['PUT'])
@jwt_required()
def update_producto(id_producto):
    data = request.get_json()
    
    try:
        with get_session() as session:
            producto = session.query(Producto).get(id_producto)
            if producto is None:
                return jsonify({'error': 'Producto no encontrado'}), 404
            
            # Actualizar los campos si se proporcionan en la solicitud
            nombre = data.get('nombre')
            if nombre:
                producto.nombre = nombre
            
            descripcion = data.get('descripcion')
            if descripcion is not None:
                producto.descripcion = descripcion
            
            precio = data.get('precio')
            if precio:
                producto.precio = precio
            
            puntos_necesario = data.get('puntos_necesario')
            if puntos_necesario is not None:
                producto.puntos_necesario = puntos_necesario
            
            foto_url = data.get('foto_url')
            if foto_url is not None:
                producto.foto_url = foto_url
            
            disponibilidad = data.get('disponibilidad')
            if disponibilidad is not None:
                producto.disponibilidad = disponibilidad
            
            descuento = data.get('descuento')
            if descuento is not None:
                producto.descuento = descuento
            
            # Si se proporciona id_categoria, verificar que exista
            id_categoria = data.get('id_categoria')
            if id_categoria is not None:
                if id_categoria:
                    categoria = session.query(Categoria).get(id_categoria)
                    if categoria is None:
                        return jsonify({'error': 'Categoría no encontrada'}), 404
                    producto.id_categoria = id_categoria
                else:
                    # Permitir que id_categoria sea NULL
                    producto.id_categoria = None
            
            # Si se proporciona id_local, verificar que exista
            id_local = data.get('id_local')
            if id_local is not None:
                local = session.query(Local).get(id_local)
                if local is None:
                    return jsonify({'error': 'Local no encontrado'}), 404
                producto.id_local = id_local
            
            session.commit()
            return jsonify(producto.serialize()), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un producto
@producto_bp.route('/producto/<int:id_producto>', methods=['DELETE'])
@jwt_required()
def delete_producto(id_producto):
    try:
        with get_session() as session:
            producto = session.query(Producto).get(id_producto)
            if producto is None:
                return jsonify({'error': 'Producto no encontrado'}), 404
            
            session.delete(producto)
            session.commit()
            return jsonify({'message': 'Producto eliminado correctamente'}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

# Nueva ruta para obtener productos por id_local (sin autenticación)
@producto_bp.route('/productos/local/<int:id_local>', methods=['GET'])
def get_productos_por_local(id_local):
    try:
        with get_session() as session:
            # Verificar que el local existe
            local = session.query(Local).get(id_local)
            if local is None:
                return jsonify({'error': 'Local no encontrado'}), 404

            productos = session.query(Producto).filter_by(id_local=id_local).all()
            if not productos:
                return jsonify({'message': 'No se encontraron productos para este local'}), 404

            resultado = [producto.serialize() for producto in productos]
            return jsonify(resultado), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
