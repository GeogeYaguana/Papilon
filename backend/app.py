# app.py
from flask import Flask
from config import Config
from extensions import bcrypt, jwt, Base, engine
from routes import register_blueprints
from flask_cors import CORS
import socket

def get_local_ip():
    """Obtiene la dirección IP local de la máquina."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:8081","http://localhost:3000","http://localhost:5000"]}})
    bcrypt.init_app(app)
    jwt.init_app(app)
    register_blueprints(app)

    # Crear las tablas en la base de datos si no existen
    with app.app_context():
        Base.metadata.create_all(bind=engine)
    @app.route('/')
    def home():
        return "Bienvenido al backend de papilon xd"
    return app

app = create_app()

if __name__ == '__main__':
    local_ip = get_local_ip()
    print(f" * La aplicación Flask está disponible en:\n")
    print(f" * Local:      http://127.0.0.1:5000")
    print(f" * Red local:  http://{local_ip}:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
