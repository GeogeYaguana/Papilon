'''from flask import Blueprint, request, jsonify
from models import DetalleFactura, Factura, Producto
from extensions import get_session
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

detalle_factura_bp = Blueprint('detalle_factura_bp', __name__)

@detalle_factura_bp.route('/detalles_factura', methods=['GET'])
@jwt_required()
def get_detalles_factura():
    with get_session() as session:
        detalles = session.query(DetalleFactura).all()
        return jsonify([detalle.serialize() for detalle in detalles]), 200

@detalle_factura_bp.route('/detalles_factura', methods=['POST'])
@jwt_required()
def create_detalle_factura():
    data = request.get_json()
    id_factura = data.get('id_factura')
    id_producto = data.get('id_producto')
    cantidad = data.get('cantidad')

    with get_session() as session:
        # Validar que la factura exista
        factura = session.query(Factura).get(id_factura)
        if not factura:
            return jsonify({'error': 'Factura no encontrada'}), 404

        # Validar que el producto exista
        producto = session.query(Producto).get(id_producto)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404

        nuevo_detalle = DetalleFactura(
            id_factura=factura.id_factura,
            id_producto=producto.id_producto,
            precio_unitario=producto.precio,
            cantidad=cantidad
        )

        try:
            session.add(nuevo_detalle)
            session.commit()
            return jsonify({'mensaje': 'Detalle de factura creado', 'id_detalle_factura': nuevo_detalle.id_detalle_factura}), 201
        except SQLAlchemyError:
            session.rollback()
            return jsonify({'error': 'Error al crear el detalle de factura'}), 400


@detalle_factura_bp.route('/detalles_factura/<int:id_detalle_factura>', methods=['DELETE'])
@jwt_required()
def delete_detalle_factura(id_detalle_factura):
    with get_session() as session:
        detalle = session.query(DetalleFactura).get(id_detalle_factura)
        if not detalle:
            return jsonify({'error': 'Detalle de factura no encontrado'}), 404

        try:
            session.delete(detalle)
            session.commit()
            return jsonify({'mensaje': 'Detalle de factura eliminado'}), 200
        except SQLAlchemyError:
            session.rollback()
            return jsonify({'error': 'Error al eliminar el detalle de factura'}), 400
'''