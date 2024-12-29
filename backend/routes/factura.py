from flask import Blueprint, request, jsonify
from models import Factura, Cliente, Local , DetalleFactura
from extensions import get_session
from sqlalchemy.exc import SQLAlchemyError

factura_bp = Blueprint('factura_bp', __name__)

@factura_bp.route('/facturas', methods=['POST'])
def create_factura_with_detalle():
    data = request.get_json()
    id_cliente = data.get('id_cliente')
    estado = data.get('estado')
    total = data.get('total')
    detalle_facturas = data.get('detalle_facturas')
    id_usuario_local = data.get('id_usuario_local')

    # Validaciones iniciales
    if not detalle_facturas or not isinstance(detalle_facturas, list):
        return jsonify({'error': 'Se requiere al menos un detalle de factura'}), 400
    if not id_usuario_local:
        return jsonify({'error': 'El ID del usuario local es obligatorio'}), 400

    with get_session() as session:
        # Verificar cliente y local
        cliente = session.query(Cliente).get(id_cliente)
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        local = session.query(Local).filter_by(id_usuario=id_usuario_local).first()
        if not local:
            return jsonify({
                'error': 'Local asociado al usuario no encontrado',
                'details': f'No se encontró un local para el usuario con ID {id_usuario_local}'
            }), 404

        # Crear la nueva factura
        nueva_factura = Factura(
            id_cliente=id_cliente,
            id_local=local.id_local,
            estado=estado,
            total=total
        )

        try:
            # Agregar factura
            session.add(nueva_factura)
            session.flush()

            # Crear los detalles de la factura
            for detalle_data in detalle_facturas:
                id_producto = detalle_data.get('id_producto')
                precio_unitario = detalle_data.get('precio_unitario')
                cantidad = detalle_data.get('cantidad')

                if not id_producto or not precio_unitario or not cantidad:
                    return jsonify({'error': 'Faltan campos en detalle de factura'}), 400

                nuevo_detalle = DetalleFactura(
                    id_factura=nueva_factura.id_factura,
                    id_producto=id_producto,
                    precio_unitario=precio_unitario,
                    cantidad=cantidad
                )
                session.add(nuevo_detalle)

            # Confirmar transacción
            session.commit()

            # Serializar datos
            factura_data = nueva_factura.serialize()
            factura_data['detalle_facturas'] = [
                detalle.serialize() for detalle in session.query(DetalleFactura).filter_by(id_factura=nueva_factura.id_factura).all()
            ]

            return jsonify({
                'message': 'Factura y detalles creados exitosamente',
                'factura': factura_data
            }), 201

        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

@factura_bp.route('/facturas/<int:id_factura>', methods=['GET'])
def get_factura(id_factura):
    with get_session() as session:
        factura = session.query(Factura).get(id_factura)
        if not factura:
            return jsonify({'error': 'Factura no encontrada'}), 404
        return jsonify(factura.serialize()), 200

@factura_bp.route('/facturas/<int:id_factura>', methods=['DELETE'])
def delete_factura(id_factura):
    with get_session() as session:
        factura = session.query(Factura).get(id_factura)
        if not factura:
            return jsonify({'error': 'Factura no encontrada'}), 404

        try:
            session.delete(factura)
            session.commit()
            return jsonify({'message': 'Factura eliminada correctamente'}), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
detalle_factura_bp = Blueprint('detalle_factura_bp', __name__)

@detalle_factura_bp.route('/detalle_facturas', methods=['POST'])
def create_detalle_factura():
    data = request.get_json()
    id_factura = data.get('id_factura')
    id_producto = data.get('id_producto')
    precio_unitario = data.get('precio_unitario')
    cantidad = data.get('cantidad')

    with get_session() as session:
        detalle = DetalleFactura(
            id_factura=id_factura,
            id_producto=id_producto,
            precio_unitario=precio_unitario,
            cantidad=cantidad
        )

        try:
            session.add(detalle)
            session.commit()
            return jsonify(detalle.serialize()), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

@detalle_factura_bp.route('/detalle_facturas/<int:id_detalle_factura>', methods=['GET'])
def get_detalle_factura(id_detalle_factura):
    with get_session() as session:
        detalle = session.query(DetalleFactura).get(id_detalle_factura)
        if not detalle:
            return jsonify({'error': 'Detalle de factura no encontrado'}), 404
        return jsonify(detalle.serialize()), 200

@detalle_factura_bp.route('/detalle_facturas/<int:id_detalle_factura>', methods=['DELETE'])
def delete_detalle_factura(id_detalle_factura):
    with get_session() as session:
        detalle = session.query(DetalleFactura).get(id_detalle_factura)
        if not detalle:
            return jsonify({'error': 'Detalle de factura no encontrado'}), 404

        try:
            session.delete(detalle)
            session.commit()
            return jsonify({'message': 'Detalle de factura eliminado correctamente'}), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
@factura_bp.route('/facturas/usuario/<int:id_usuario>', methods=['GET'])
def get_facturas_by_usuario(id_usuario):
    with get_session() as session:
        # Verificar si el usuario está asociado a un cliente
        local = session.query(Local).filter_by(id_usuario=id_usuario).first()
        if not local:
            return jsonify({'error': 'Usuario no asociado a un cliente válido'}), 404

        # Obtener todas las facturas del cliente
        facturas = session.query(Factura).filter_by(id_local=local.id_local).all()
        if not facturas:
            return jsonify({'message': 'No se encontraron facturas para este usuario'}), 404

        # Serializar facturas y sus detalles
        resultado = []
        for factura in facturas:
            detalles = session.query(DetalleFactura).filter_by(id_factura=factura.id_factura).all()
            factura_data = factura.serialize()
            factura_data['detalle_facturas'] = [detalle.serialize() for detalle in detalles]
            resultado.append(factura_data)

        return jsonify({'facturas': resultado}), 200
@factura_bp.route('/facturas/<int:id_factura>', methods=['PUT'])
def update_factura(id_factura):
    data = request.get_json()
    estado = data.get('estado')
    total = data.get('total')
    puntos_ganados = data.get('puntos_ganados')

    with get_session() as session:
        factura = session.query(Factura).get(id_factura)
        if not factura:
            return jsonify({'error': 'Factura no encontrada'}), 404

        if estado is not None:
            factura.estado = estado
        if total is not None:
            factura.total = total
        if puntos_ganados is not None:
            factura.puntos_ganados = puntos_ganados

        try:
            session.commit()
            return jsonify({
                'message': 'Factura actualizada exitosamente',
                'factura': factura.serialize()
            }), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

