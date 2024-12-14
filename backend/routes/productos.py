from flask import Blueprint, request, jsonify
from models import Producto, Local, Categoria
from extensions import get_session
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity

productos_bp = Blueprint('producto_bp', __name__)

# Función para crear un producto donde el ID del local se asigna según el usuario en sesión
@productos_bp.route('/crear_producto_sesion', methods=['POST'])
@jwt_required()
def create_producto_sesion():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    puntos_necesario = data.get('puntos_necesario')
    foto_url = data.get('foto_url')
    disponibilidad = data.get('disponibilidad', True)
    descuento = data.get('descuento')
    id_categoria = data.get('id_categoria')

    current_user_id = get_jwt_identity()

    with get_session() as session:
        # Buscar el local asociado al usuario en sesión
        usuario = session.query(usuario).get(current_user_id)
        if not usuario or usuario.tipo_usuario != 'local':
            return jsonify({'error': 'El usuario debe ser de tipo local'}), 403

        local = session.query(Local).filter_by(id_usuario=usuario.id_usuario).first()
        if not local:
            return jsonify({'error': 'No se encontró un local asociado al usuario'}), 404

        # Crear el producto con el local asociado
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            puntos_necesario=puntos_necesario,
            foto_url=foto_url,
            disponibilidad=disponibilidad,
            descuento=descuento,
            id_local=local.id_local,
            id_categoria=id_categoria
        )

        try:
            session.add(nuevo_producto)
            session.commit()
            return jsonify({
                'mensaje': 'Producto creado correctamente',
                'id_producto': nuevo_producto.id_producto
            }), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

# Función para crear un producto donde el ID del local se asigna según el ID proporcionado
@productos_bp.route('/crear_producto_local', methods=['POST'])
@jwt_required()
def create_producto_local():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    puntos_necesario = data.get('puntos_necesario')
    foto_url = data.get('foto_url')
    disponibilidad = data.get('disponibilidad', True)
    descuento = data.get('descuento')
    id_categoria = data.get('id_categoria')
    id_local = data.get('id_local')

    with get_session() as session:
        # Verificar si el local existe
        local = session.query(Local).get(id_local)
        if not local:
            return jsonify({'error': 'Local no encontrado'}), 404

        # Crear el producto con el local especificado
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            puntos_necesario=puntos_necesario,
            foto_url=foto_url,
            disponibilidad=disponibilidad,
            descuento=descuento,
            id_local=id_local,
            id_categoria=id_categoria
        )

        try:
            session.add(nuevo_producto)
            session.commit()
            return jsonify({
                'mensaje': 'Producto creado correctamente',
                'id_producto': nuevo_producto.id_producto
            }), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

# Función para obtener todos los productos
@productos_bp.route('/productos', methods=['GET'])
@jwt_required()
def get_productos():
    with get_session() as session:
        productos = session.query(Producto).all()
        resultado = []

        for producto in productos:
            local = session.query(Local).get(producto.id_local)
            categoria = session.query(Categoria).get(producto.id_categoria)
            if local and categoria:
                producto_data = producto.serialize()
                producto_data['local'] = {
                    'id_local': local.id_local,
                    'nombre_local': local.nombre_local,
                    'direccion': local.direccion
                }
                producto_data['categoria'] = {
                    'id_categoria': categoria.id_categoria,
                    'nombre': categoria.nombre
                }
                resultado.append(producto_data)

        return jsonify(resultado), 200

# Función para obtener un producto por su ID
@productos_bp.route('/productos/<int:id_producto>', methods=['GET'])
@jwt_required()
def get_producto(id_producto):
    with get_session() as session:
        producto = session.query(Producto).get(id_producto)
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404

        local = session.query(Local).get(producto.id_local)
        categoria = session.query(Categoria).get(producto.id_categoria)
        if not local or not categoria:
            return jsonify({'error': 'Local o categoria asociados no encontrados'}), 404

        producto_data = producto.serialize()
        producto_data['local'] = {
            'id_local': local.id_local,
            'nombre_local': local.nombre_local,
            'direccion': local.direccion
        }
        producto_data['categoria'] = {
            'id_categoria': categoria.id_categoria,
            'nombre': categoria.nombre
        }

        return jsonify(producto_data), 200

# Función para actualizar un producto
@productos_bp.route('/productos/<int:id_producto>', methods=['PUT'])
@jwt_required()
def update_producto(id_producto):
    data = request.get_json()

    with get_session() as session:
        producto = session.query(Producto).get(id_producto)
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404

        # Actualizar campos del Producto
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        precio = data.get('precio')
        puntos_necesario = data.get('puntos_necesario')
        foto_url = data.get('foto_url')
        disponibilidad = data.get('disponibilidad', True)
        descuento = data.get('descuento')
        id_categoria = data.get('id_categoria')

        if nombre is not None:
            producto.nombre = nombre
        if descripcion is not None:
            producto.descripcion = descripcion
        if precio is not None:
            producto.precio = precio
        if puntos_necesario is not None:
            producto.puntos_necesario = puntos_necesario
        if foto_url is not None:
            producto.foto_url = foto_url
        if disponibilidad is not None:
            producto.disponibilidad = disponibilidad
        if descuento is not None:
            producto.descuento = descuento
        if id_categoria is not None:
            producto.id_categoria = id_categoria

        try:
            session.commit()
            return jsonify({
                'mensaje': 'Producto actualizado correctamente',
                'id_producto': producto.id_producto
            }), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

# Función para eliminar un producto
@productos_bp.route('/productos/<int:id_producto>', methods=['DELETE'])
@jwt_required()
def delete_producto(id_producto):
    with get_session() as session:
        producto = session.query(Producto).get(id_producto)
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404

        try:
            session.delete(producto)
            session.commit()
            return jsonify({'mensaje': 'Producto eliminado exitosamente'}), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
