'''from flask import Blueprint, request, jsonify
from models import Canje, Cliente, Local
from extensions import get_session
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity

canje_bp = Blueprint('canje_bp', __name__)

@canje_bp.route('/canjes', methods=['GET'])
@jwt_required()
def get_canjes():
    with get_session() as session:
        canjes = session.query(Canje).all()
        return jsonify([canje.serialize() for canje in canjes]), 200

@canje_bp.route('/crear_canje', methods=['POST'])
@jwt_required()
def create_canje():
    data = request.get_json()
    id_local = data.get('id_local')
    puntos_utilizados = data.get('puntos_utilizados')

    current_user_id = get_jwt_identity()

    with get_session() as session:
        # Verificar si el usuario actual es cliente
        cliente = session.query(Cliente).filter_by(id_usuario=current_user_id).first()
        if not cliente:
            return jsonify({'error': 'El usuario no es un cliente válido'}), 403

        # Verificar que el cliente tenga suficientes puntos
        if cliente.puntos < puntos_utilizados:
            return jsonify({'error': 'Puntos insuficientes'}), 400

        # Verificar si el local existe
        local = session.query(Local).get(id_local)
        if not local:
            return jsonify({'error': 'Local no encontrado'}), 404

        # Crear el nuevo canje
        nuevo_canje = Canje(
            id_cliente=cliente.id_cliente,
            id_local=id_local,
            estado='pendiente',
            puntos_utilizados=puntos_utilizados
        )

        try:
            # Restar los puntos utilizados del cliente
            cliente.puntos -= puntos_utilizados

            # Guardar el canje y actualizar la tabla cliente
            session.add(nuevo_canje)
            session.commit()

            return jsonify({
                'mensaje': 'Canje creado exitosamente',
                'id_canje': nuevo_canje.id_canje
            }), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': 'Error al crear el canje'}), 400
'''