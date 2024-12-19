import pytest
from app import create_app
from models import Base, Usuario, Local, Producto, Categoria
from extensions import SessionLocal, engine
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown_database():
    """Elimina y recrea las tablas antes y después de cada prueba."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_token():
    """Crea un token JWT para un usuario local."""
    with SessionLocal() as session:
        # Crear usuario de tipo local
        usuario = Usuario(usuario_nombre="local_test", contrasena="hashed_password", tipo_usuario="local")
        session.add(usuario)
        session.commit()

        # Crear local asociado al usuario
        local = Local(id_usuario=usuario.id_usuario, nombre_local="Local Test", direccion="Direccion Test")
        session.add(local)
        session.commit()

        # Crear token
        token = create_access_token(identity=usuario.id_usuario)
        return token

def test_create_producto_sesion(client, auth_token):
    """Prueba la creación de un producto asociado al usuario en sesión."""
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Crear categoría para asociar al producto
    with SessionLocal() as session:
        categoria = Categoria(nombre="Categoria Test")
        session.add(categoria)
        session.commit()

    # Datos del producto
    producto_data = {
        "nombre": "Producto Test",
        "descripcion": "Descripción del producto",
        "precio": 100.00,
        "puntos_necesario": 10,
        "foto_url": "http://example.com/foto.jpg",
        "disponibilidad": True,
        "descuento": 5.00,
        "id_categoria": categoria.id_categoria,
    }

    response = client.post("/crear_producto_sesion", json=producto_data, headers=headers)

    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["mensaje"] == "Producto creado correctamente"
    assert "id_producto" in response_data

def test_get_productos(client, auth_token):
    """Prueba la obtención de todos los productos."""
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Crear categoría y producto para la prueba
    with SessionLocal() as session:
        categoria = Categoria(nombre="Categoria Test")
        session.add(categoria)
        session.commit()

        local = session.query(Local).first()
        producto = Producto(
            nombre="Producto Test",
            descripcion="Descripción del producto",
            precio=100.00,
            puntos_necesario=10,
            foto_url="http://example.com/foto.jpg",
            disponibilidad=True,
            descuento=5.00,
            id_local=local.id_local,
            id_categoria=categoria.id_categoria,
        )
        session.add(producto)
        session.commit()

    response = client.get("/productos", headers=headers)

    assert response.status_code == 200
    response_data = response.get_json()
    assert len(response_data) == 1
    assert response_data[0]["nombre"] == "Producto Test"
