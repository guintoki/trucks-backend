from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

# Inicializa o SQLAlchemy
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializa as extensões
    CORS(app, 
         resources={r"/*": {
             "origins": ["http://localhost:3000"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }})
    db.init_app(app)
    
    # Registra os blueprints
    from app.routes import drivers, trucks, assignments
    app.register_blueprint(drivers.bp)
    app.register_blueprint(trucks.bp)
    app.register_blueprint(assignments.bp)
    
    # Cria as tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    # Configura o Flask para lidar com rotas com ou sem barra no final
    app.url_map.strict_slashes = False
    
    return app 