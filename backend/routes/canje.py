from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import Canje, Cliente, Local , Producto , DetalleCanje , Usuario
from extensions import get_session

canje_bp = Blueprint('canje_bp', __name__)

@canje_bp.route('/canjes', methods=['POST'])
def create_canje():
    data = request.get_json()
    id_cliente = data.get('id_cliente')
    id_local = data.get('id_local')
    estado = data.get('estado')
    puntos_utilizados = data.get('puntos_utilizados')

    with get_session() as session:
        cliente = session.query(Cliente).get(id_cliente)
        local = session.query(Local).get(id_local)

        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        if not local:
            return jsonify({'error': 'Local no encontrado'}), 404

        nuevo_canje = Canje(
            id_cliente=id_cliente,
            id_local=id_local,
            estado=estado,
            puntos_utilizados=puntos_utilizados
        )

        try:
            session.add(nuevo_canje)
            session.commit()
            return jsonify(nuevo_canje.serialize()), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

@canje_bp.route('/realizar_canje', methods=['POST'])
def realizar_canje():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    id_producto = data.get('id_producto')
    cantidad = data.get('cantidad', 1)

    if not id_usuario or not id_producto:
        return jsonify({'error': 'id_usuario y id_producto son requeridos'}), 400

    with get_session() as session:
        try:
            # Verificar si el usuario está asociado a un cliente
            cliente = session.query(Cliente).filter_by(id_usuario=id_usuario).first()
            if not cliente:
                return jsonify({'error': 'El usuario no está asociado a un cliente válido'}), 404

            # Obtener el producto
            producto = session.query(Producto).get(id_producto)
            if not producto:
                return jsonify({'error': 'Producto no encontrado'}), 404

            # Verificar si el producto tiene puntos necesarios
            if producto.puntos_necesario is None:
                return jsonify({'error': 'El producto no permite canje por puntos'}), 400

            # Verificar si el cliente tiene puntos suficientes
            puntos_totales = producto.puntos_necesario * cantidad
            if cliente.puntos < puntos_totales:
                return jsonify({'error': 'El cliente no tiene suficientes puntos para realizar el canje'}), 400

            # Obtener el local que ofrece el producto
            local = session.query(Local).get(producto.id_local)
            if not local:
                return jsonify({'error': 'Local asociado al producto no encontrado'}), 404

            # Crear el canje
            nuevo_canje = Canje(
                id_cliente=cliente.id_cliente,
                id_local=local.id_local,
                estado='pendiente',
                puntos_utilizados=puntos_totales
            )
            session.add(nuevo_canje)
            session.flush()

            # Crear el detalle de canje
            detalle_canje = DetalleCanje(
                id_canje=nuevo_canje.id_canje,
                id_producto=id_producto,
                cantidad=cantidad,
                puntos_totales=puntos_totales,
                valor=producto.precio * cantidad
            )
            session.add(detalle_canje)

            # Confirmar transacción
            session.commit()

            return jsonify({
                'message': 'Canje y detalle registrados exitosamente',
                'canje': nuevo_canje.serialize(),
                'detalle_canje': detalle_canje.serialize()
            }), 201

        except SQLAlchemyError as e:
            session.rollback()  # Revertir transacción en caso de error
            return jsonify({'error': str(e)}), 500
        except Exception as e:
            session.rollback()  # Revertir transacción en caso de cualquier otra excepción
            return jsonify({'error': 'Error inesperado: ' + str(e)}), 500


@canje_bp.route('/canjes/<int:id_canje>', methods=['PUT'])
def update_estado_canje(id_canje):
    data = request.get_json()
    nuevo_estado = data.get('estado')

    if not nuevo_estado:
        return jsonify({'error': 'El estado es obligatorio'}), 400

    with get_session() as session:
        try:
            # Buscar el canje por su ID
            canje = session.query(Canje).get(id_canje)
            if not canje:
                return jsonify({'error': 'Canje no encontrado'}), 404

            # Validar el nuevo estado
            estados_validos = ['pendiente', 'completado', 'cancelado']
            if nuevo_estado not in estados_validos:
                return jsonify({'error': f'Estado inválido. Estados válidos: {", ".join(estados_validos)}'}), 400

            # Actualizar el estado del canje
            canje.estado = nuevo_estado
            session.commit()

            return jsonify({
                'message': 'Estado del canje actualizado correctamente',
                'canje': canje.serialize()
            }), 200

        except SQLAlchemyError as e:
            session.rollback()  # Revertir la transacción en caso de error
            return jsonify({'error': str(e)}), 500
        except Exception as e:
            session.rollback()  # Revertir la transacción en caso de cualquier otra excepción
            return jsonify({'error': 'Error inesperado: ' + str(e)}), 500
# Ruta para obtener canjes asociados a un local
@canje_bp.route('/canjes/local/usuario/<int:id_usuario>', methods=['GET'])
def get_canjes_by_local(id_usuario):
    with get_session() as session:
        # Verificar si el usuario está asociado a un local
        local = session.query(Local).filter_by(id_usuario=id_usuario).first()
        if not local:
            return jsonify({'error': 'El usuario no está asociado a un local válido'}), 404

        # Obtener todos los canjes asociados al local
        canjes = session.query(Canje).filter_by(id_local=local.id_local).all()

        if not canjes:
            return jsonify({'message': 'No se encontraron canjes para este local'}), 404

        # Serializar los canjes con sus detalles
        resultado = []
        for canje in canjes:
            detalles_canje = [
                {
                    'id_detalle_canje': detalle.id_detalle_canje,
                    'id_producto': detalle.id_producto,
                    'cantidad': detalle.cantidad,
                    'puntos_totales': detalle.puntos_totales,
                    'valor': str(detalle.valor),
                    'fecha_creacion': detalle.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if detalle.fecha_creacion else None,
                    'producto': {
                        'id_producto': detalle.producto.id_producto,
                        'nombre': detalle.producto.nombre,
                        'puntos_necesario': detalle.producto.puntos_necesario
                    }
                }
                for detalle in canje.detalles
            ]

            canje_data = {
                'id_canje': canje.id_canje,
                'id_cliente': canje.id_cliente,
                'id_local': canje.id_local,
                'estado': canje.estado,
                'puntos_utilizados': canje.puntos_utilizados,
                'fecha': canje.fecha.strftime("%Y-%m-%d %H:%M:%S") if canje.fecha else None,
                'local': {
                    'id_local': local.id_local,
                    'nombre_local': local.nombre_local,
                    'direccion': local.direccion
                },
                'detalles': detalles_canje
            }

            resultado.append(canje_data)

        return jsonify({'canjes': resultado}), 200

# Ruta para obtener canjes asociados a un cliente
@canje_bp.route('/canjes/cliente/usuario/<int:id_usuario>', methods=['GET'])
def get_canjes_by_cliente(id_usuario):
    with get_session() as session:
        # Verificar si el usuario está asociado a un cliente
        cliente = session.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if not cliente:
            return jsonify({'error': 'El usuario no está asociado a un cliente válido'}), 404

        # Obtener todos los canjes asociados al cliente
        canjes = session.query(Canje).filter_by(id_cliente=cliente.id_cliente).all()

        if not canjes:
            return jsonify({'message': 'No se encontraron canjes para este cliente'}), 404

        # Serializar los canjes con sus detalles
        resultado = []
        for canje in canjes:
            local = session.query(Local).filter_by(id_local=canje.id_local).first()
            detalles_canje = [
                {
                    'id_detalle_canje': detalle.id_detalle_canje,
                    'id_producto': detalle.id_producto,
                    'cantidad': detalle.cantidad,
                    'puntos_totales': detalle.puntos_totales,
                    'valor': str(detalle.valor),
                    'fecha_creacion': detalle.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if detalle.fecha_creacion else None,
                    'producto': {
                        'id_producto': detalle.producto.id_producto,
                        'nombre': detalle.producto.nombre,
                        'puntos_necesario': detalle.producto.puntos_necesario
                    }
                }
                for detalle in canje.detalles
            ]

            canje_data = {
                'id_canje': canje.id_canje,
                'id_cliente': canje.id_cliente,
                'id_local': canje.id_local,
                'estado': canje.estado,
                'puntos_utilizados': canje.puntos_utilizados,
                'fecha': canje.fecha.strftime("%Y-%m-%d %H:%M:%S") if canje.fecha else None,
                'local': {
                    'id_local': local.id_local,
                    'nombre_local': local.nombre_local,
                    'direccion': local.direccion
                } if local else None,
                'detalles': detalles_canje
            }

            resultado.append(canje_data)

        return jsonify({'canjes': resultado}), 200

