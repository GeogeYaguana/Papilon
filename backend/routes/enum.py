from flask import Blueprint, jsonify
from sqlalchemy.dialects.postgresql import ENUM
from extensions import get_session
from sqlalchemy.sql import text
enum_bp = Blueprint('enum_bp', __name__)

def get_enum_values(enum_type):
    with get_session() as session:
        # Consulta SQL explícita declarada con text()
        query = text(f"""
            SELECT unnest(enum_range(NULL::{enum_type}));
        """)
        result = session.execute(query)
        # Extraer los valores del resultado
        return [row[0] for row in result.fetchall()]

@enum_bp.route('/enums/estado_canje', methods=['GET'])
def get_estado_canje_enum():
    try:
        valores = get_enum_values('estado_canje_enum')
        return jsonify({'enum': 'estado_canje_enum', 'values': valores}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enum_bp.route('/enums/estado_factura', methods=['GET'])
def get_estado_factura_enum():
    try:
        valores = get_enum_values('estado_factura_enum')
        return jsonify({'enum': 'estado_factura_enum', 'values': valores}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

