from flask import Blueprint, request, jsonify
from models import Factura, Local, Cliente
from extensions import get_session
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity

factura_bp = Blueprint('factura_bp', __name__)

@factura_bp.route('/facturas', methods=['GET'])
@jwt_required()
def get_facturas():
    with get_session() as session:
        facturas = session.query(Factura).all()
        return jsonify([factura.serialize() for factura in facturas]), 200

@factura_bp.route('/facturas/<int:id_factura>', methods=['GET'])
@jwt_required()
def get_factura(id_factura):
    with get_session() as session:
        factura = session.query(Factura).get(id_factura)
        if factura is None:
            return jsonify({'error': 'Factura no encontrada'}), 404
        return jsonify(factura.serialize()), 200

@factura_bp.route('/facturas', methods=['POST'])
@jwt_required()
def create_factura():
    data = request.get_json()
    id_cliente = data.get('id_cliente')
    total = data.get('total')
    estado = data.get('estado')

    current_user_id = get_jwt_identity()

    with get_session() as session:
        # Validar que el cliente exista
        cliente = session.query(Cliente).get(id_cliente)
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        # Obtener el local asociado al usuario en sesión
        local = session.query(Local).filter_by(id_usuario=current_user_id).first()
        if not local:
            return jsonify({'error': 'El usuario no tiene un local asociado'}), 404

        nueva_factura = Factura(
            id_local=local.id_local,
            id_cliente=cliente.id_cliente,
            total=total,
            estado=estado
        )

        try:
            session.add(nueva_factura)
            session.commit()
            return jsonify({'mensaje': 'Factura creada', 'id_factura': nueva_factura.id_factura}), 201
        except SQLAlchemyError:
            session.rollback()
            return jsonify({'error': 'Error al crear la factura'}), 400


@factura_bp.route('/facturas/<int:id_factura>', methods=['PUT'])
@jwt_required()
def update_factura(id_factura):
    data = request.get_json()
    estado = data.get('estado')

    with get_session() as session:
        factura = session.query(Factura).get(id_factura)
        if factura is None:
            return jsonify({'error': 'Factura no encontrada'}), 404

        if estado is not None:
            factura.estado = estado

        try:
            session.commit()
            return jsonify({'mensaje': 'Factura actualizada'}), 200
        except SQLAlchemyError:
            session.rollback()
            return jsonify({'error': 'Error al actualizar la factura'}), 400

@factura_bp.route('/facturas/<int:id_factura>', methods=['DELETE'])
@jwt_required()
def delete_factura(id_factura):
    with get_session() as session:
        factura = session.query(Factura).get(id_factura)
        if factura is None:
            return jsonify({'error': 'Factura no encontrada'}), 404

        try:
            session.delete(factura)
            session.commit()
            return jsonify({'mensaje': 'Factura eliminada'}), 200
        except SQLAlchemyError:
            session.rollback()
            return jsonify({'error': 'Error al eliminar la factura'}), 400
