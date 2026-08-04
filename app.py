import os
from config import Config
from src import create_app

app = create_app()

if __name__ == '__main__':
    # Configuracion para producción
    port = int(os.environ.get('PORT', Config.PORT)) 
    debug = os.environ.get('FLASK_ENV') != 'production' 

    print("Iniciando RedCode Academy...") 
    print(f"Servidor corriendo en: http://{Config.HOST}:{Config.PORT}") 
    print(f"Base de datos configurada: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"Servidor corriendo en: http://{Config.HOST}:{port}")
    print("Presiona Ctrl+C para detener el servidor") 

    # Iniciar el servidor Flask 
    app.run( 
        host=Config.HOST,      # 0.0.0.0 permite conexiones externas 
        port=port,      # Puerto configurado (5000 por defecto) 
        debug=Config.DEBUG     # Modo debug para desarrollo 
    )
    