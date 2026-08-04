import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src import create_app
from config import Config

class TestConfig(Config):
    """Configuración específica para el entorno de pruebas."""
    TESTING = True
    # Usar base de datos en memoria para pruebas rápidas e independientes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Desactivar protección CSRF en testing para facilitar las peticiones POST
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'

@pytest.fixture
def app():
    """Crea y configura una nueva instancia de la aplicación Flask para cada prueba."""
    app = create_app()
    app.config.from_object(TestConfig)

    # Aquí puedes añadir código para inicializar la base de datos de prueba
    # con app.app_context():
    #     db.create_all()
    #     yield app
    #     db.drop_all()
    
    yield app

@pytest.fixture
def client(app):
    """Un cliente de pruebas para la aplicación."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Un runner de pruebas para comandos CLI (e.g., comandos flask)."""
    return app.test_cli_runner()

@pytest.fixture
def auth(client):
    """Helper de autenticación para facilitar el inicio y cierre de sesión en los tests."""
    class AuthActions:
        def __init__(self, client):
            self._client = client

        def login(self, email='test@example.com', password='password'):
            # Realiza un POST a la ruta de login
            return self._client.post(
                '/login',
                data={'email': email, 'password': password}
            )

        def logout(self):
            return self._client.get('/logout')
            
    return AuthActions(client)
