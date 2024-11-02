# routes/__init__.py
def register_blueprints(app):
    from .auth import auth_bp
    from .usuarios import usuario_bp
    from .local import local_bp
    from .cliente import cliente_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(local_bp)
    app.register_blueprint(cliente_bp)