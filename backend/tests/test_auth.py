# test_auth.py

import pytest
from flask import Flask
from flask.testing import FlaskClient
from extensions import bcrypt, jwt
from models import Base, Usuario
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from extensions import get_session


from routes.auth import auth_bp

# Configuración de prueba
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test_user:test_password@localhost/test_db'
    JWT_SECRET_KEY = 'test_jwt_secret_key'

@pytest.fixture
def app():
    # Crear la aplicación Flask y configurar para pruebas
    app = Flask(__name__)
    app.config.from_object(TestConfig)

    # Inicializar extensiones
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Registrar blueprints
    from routes import register_blueprints
    register_blueprints(app)

    # Configurar la base de datos para pruebas
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Reemplazar get_session en el módulo extensions
    import extensions
    def override_get_session():
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
    extensions.get_session = override_get_session

    # Contexto de aplicación para pruebas
    with app.app_context():
        yield app

    # Teardown: eliminar las tablas después de las pruebas
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(app):
    return app.test_client()


def test_login_successful(client, app):
    # Agregar un usuario de prueba a la base de datos
    with app.app_context():
        with get_session() as session:
            password_hash = bcrypt.generate_password_hash('testpassword').decode('utf-8')
            test_user = Usuario(usuario_nombre='testuser', password=password_hash, tipo_usuario='admin')
            session.add(test_user)
            session.commit()
            test_user_id = test_user.id_usuario

    # Enviar una solicitud POST a /login
    response = client.post('/login', json={
        'usuario_nombre': 'testuser',
        'password': 'testpassword'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert data['message'] == 'Inicio de sesión exitoso'
    assert data['id_usuario'] == test_user_id
    assert data['tipo_usuario'] == 'admin'

def test_login_wrong_password(client, app):
    # Agregar un usuario de prueba a la base de datos
    with app.app_context():
        with get_session() as session:
            password_hash = bcrypt.generate_password_hash('testpassword').decode('utf-8')
            test_user = Usuario(usuario_nombre='testuser', password=password_hash)
            session.add(test_user)
            session.commit()

    # Enviar una solicitud POST a /login con contraseña incorrecta
    response = client.post('/login', json={
        'usuario_nombre': 'testuser',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Usuario o contraseña incorrectos'

def test_login_nonexistent_user(client):
    # Enviar una solicitud POST a /login con usuario inexistente
    response = client.post('/login', json={
        'usuario_nombre': 'nonexistentuser',
        'password': 'testpassword'
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Usuario o contraseña incorrectos'

def test_login_missing_username(client):
    # Enviar una solicitud POST a /login sin usuario_nombre
    response = client.post('/login', json={
        'password': 'testpassword'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'usuario_nombre' in data['error']

def test_login_missing_password(client):
    # Enviar una solicitud POST a /login sin password
    response = client.post('/login', json={
        'usuario_nombre': 'testuser'
    })

    assert response.status_code == 400
    data = response.get_json()
    assert 'password' in data['error']
