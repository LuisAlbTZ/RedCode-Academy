"""
Configuración de la conexión a la base de datos y extensiones de Flask.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()

migrate = Migrate()
login_manager = LoginManager()

# Configuración de Flask-Login
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'


def init_extensions(app):
    """Inicializa todas las extensiones de Flask con la app."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Import models here so Flask-Migrate is aware of them
    from src.infrastructure.models import models


@login_manager.user_loader
def load_user(user_id: str):
    """Carga el usuario desde la base de datos para Flask-Login."""
    from src.infrastructure.models.models import Usuario
    return db.session.get(Usuario, int(user_id))