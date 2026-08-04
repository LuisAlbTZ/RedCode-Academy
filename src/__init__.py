import os
from flask import Flask, render_template 
from config import Config 

from src.infrastructure.database.connection import init_extensions

# Blueprints de las rutas 
from src.infrastructure.routes.admin_routes import admin_bp
from src.infrastructure.routes.auth_routes import auth_bp
from src.infrastructure.routes.convocatoria_routes import convocatoria_bp
from src.infrastructure.routes.main_routes import main_bp
from src.infrastructure.routes.work_group_routes import work_group_bp

def create_app():    
    # Obtener la ruta absoluta de la carpeta templates
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'presentation', 'templates')
    
    # Crear la instancia de Flask 
    app = Flask(__name__, template_folder=template_dir) 

    # Cargar configuración desde config.py (Credenciales de BD, etc.)
    app.config.from_object(Config) 

    # 1. INICIALIZAR EXTENSIONES (SQLAlchemy, Migrate, LoginManager)
    # Esto ejecuta todo el código de tu archivo connection.py
    init_extensions(app)
    
    # 2. VERIFICAR Y CREAR TABLAS DE LA BASE DE DATOS
    with app.app_context():
        # Importamos la instancia db y los modelos AQUÍ para evitar importaciones circulares
        from src.infrastructure.database.connection import db
        from src.infrastructure.models.models import (
            Usuario, Convocatoria, WorkGroup, 
            UsuarioConvocatoria, ComentarioWorkGroup, CalificacionWorkGroup
        )
        
        # Crea las tablas en MySQL automáticamente (si no existen)
        db.create_all()
     
    # 3. REGISTRAR LAS RUTAS (Blueprints)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(convocatoria_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(work_group_bp)
    
    # 4. CONFIGURAR MANEJO DE ERRORES PERSONALIZADO 
    @app.errorhandler(404) 
    def not_found_error(error): 
        """ 
        Maneja errores 404 (página no encontrada) 
        """ 
        return render_template('404.html'), 404 
     
    @app.errorhandler(500) 
    def internal_error(error): 
        """ 
        Maneja errores 500 (error interno del servidor) 
        """ 
        return render_template('500.html'), 500 
     
    return app