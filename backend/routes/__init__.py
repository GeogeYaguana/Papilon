# routes/__init__.py
def register_blueprints(app):
    from .auth import auth_bp
    from .usuarios import usuario_bp
    from .local import local_bp
    from .cliente import cliente_bp
    from .categoria import categoria_bp  
    from .productos import productos_bp
    from .factura import factura_bp
    #from .detalle_factura import detalle_factura_bp
    #from .canje import canje_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(local_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(categoria_bp) 
    app.register_blueprint(productos_bp)
    app.register_blueprint(factura_bp)
    #app.register_blueprint(detalle_factura_bp)
   # app.register_blueprint(canje_bp)