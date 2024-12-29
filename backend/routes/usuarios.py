# routes/usuario.py
from flask import Blueprint, request, jsonify
from models import Usuario
from extensions import bcrypt, get_session
from sqlalchemy.exc import SQLAlchemyError
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
        with get_session() as session:
            usuario_existente = session.query(Usuario).filter_by(usuario_nombre=usuario_nombre).first()
            if usuario_existente:
                return jsonify({'error': 'El nombre de usuario ya está en uso'}), 400
            session.add(nuevo_usuario)
            session.commit()
            return jsonify(nuevo_usuario.serialize()), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    with get_session() as session:
        usuarios = session.query(Usuario).all()
        return jsonify([usuario.serialize() for usuario in usuarios])

@usuario_bp.route('/usuario/<int:id>', methods=['GET'])
def get_usuario(id):
    with get_session() as session:
        usuario = session.query(Usuario).get(id)
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(usuario.serialize())

@usuario_bp.route('/usuario/<int:id>', methods=['PUT'])
def update_usuario(id):
    with get_session() as session:
        usuario = session.query(Usuario).get(id)
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
            session.commit()
            return jsonify(usuario.serialize())
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

@usuario_bp.route('/usuario/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    with get_session() as session:
        usuario = session.query(Usuario).get(id)
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        try:
            session.delete(usuario)
            session.commit()
            return jsonify({'message': 'Usuario eliminado correctamente'})
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

def send_email(to_email, subject, message):
    try:
        # Configuración del servidor SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "sesyaguana@gmail.com"  # Reemplaza con tu correo
        sender_password = "tu_contraseña"  # Reemplaza con tu contraseña o utiliza un token de aplicación

        # Crear el mensaje de correo
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Agregar el contenido del mensaje
        msg.attach(MIMEText(message, 'plain'))

        # Conectar al servidor SMTP y enviar el correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Inicia cifrado TLS
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

@usuario_bp.route('/usuario/recuperar-contrasena', methods=['POST'])
def solicitar_recuperacion_contrasena():
    data = request.get_json()
    correo = data.get('correo')

    if not correo:
        return jsonify({'error': 'Correo electrónico es obligatorio'}), 400

    try:
        with get_session() as session:
            usuario = session.query(Usuario).filter_by(correo=correo).first()
            if not usuario:
                return jsonify({'error': 'No se encontró un usuario con ese correo'}), 404

            # Generar código temporal o nueva contraseña
            nueva_contrasena = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            hashed_password = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')

            # Actualizar contraseña en la base de datos
            usuario.password = hashed_password
            session.commit()

            # Enviar correo con la nueva contraseña
            mensaje = f"Hola {usuario.nombre},\n\nTu nueva contraseña es: {nueva_contrasena}\nPor favor, cámbiala después de iniciar sesión."
            send_email(correo, "Recuperación de Contraseña", mensaje)

            return jsonify({'message': 'Se ha enviado un correo con la nueva contraseña'}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuario/cambiar-contrasena', methods=['PUT'])
def cambiar_contrasena():
    data = request.get_json()
    correo = data.get('correo')
    nueva_password = data.get('nueva_password')

    if not correo or not nueva_password:
        return jsonify({'error': 'Correo y nueva contraseña son obligatorios'}), 400

    try:
        with get_session() as session:
            usuario = session.query(Usuario).filter_by(correo=correo).first()
            if not usuario:
                return jsonify({'error': 'No se encontró un usuario con ese correo'}), 404

            # Actualizar la contraseña
            hashed_password = bcrypt.generate_password_hash(nueva_password).decode('utf-8')
            usuario.password = hashed_password
            session.commit()

            return jsonify({'message': 'Contraseña actualizada correctamente'}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
