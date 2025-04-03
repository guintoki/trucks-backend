from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

# Inicialização do SQLAlchemy como uma extensão Flask
# Isso permite a separação da instância do banco de dados da aplicação
db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Factory function para criar e configurar a aplicação Flask.
    Segue o padrão de aplicação factory do Flask, permitindo:
    - Múltiplas instâncias da aplicação
    - Diferentes configurações para diferentes ambientes
    - Testes mais fáceis com diferentes configurações
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configuração do CORS para desenvolvimento
    # Permite requisições do frontend em localhost:3000
    CORS(app, 
         resources={r"/*": {
             "origins": ["http://localhost:3000"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }})
    
    # Inicialização das extensões
    db.init_app(app)
    
    # Registro dos blueprints
    # Organização modular das rotas por domínio
    from app.routes import drivers, trucks, assignments
    app.register_blueprint(drivers.bp)
    app.register_blueprint(trucks.bp)
    app.register_blueprint(assignments.bp)
    
    # Criação das tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    # Configuração para aceitar rotas com ou sem barra no final
    app.url_map.strict_slashes = False
    
    return app 