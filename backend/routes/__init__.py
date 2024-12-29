# routes/__init__.py
def register_blueprints(app):
    from .auth import auth_bp
    from .usuarios import usuario_bp
    from .local import local_bp
    from .cliente import cliente_bp
    from .categoria import categoria_bp  
    from .producto import producto_bp  # Importa el Blueprint de Producto
    from routes.canje import canje_bp
    from routes.factura import factura_bp
    from routes.enum import enum_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(local_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(categoria_bp) 
    app.register_blueprint(producto_bp)  # Registra el Blueprint de Producto
    app.register_blueprint(canje_bp)
    app.register_blueprint(factura_bp)
    app.register_blueprint(enum_bp)