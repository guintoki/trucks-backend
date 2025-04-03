from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

# Inicialização do SQLAlchemy como uma extensão do Flask
# Isso permite que a instância do banco de dados seja separada da aplicação
db = SQLAlchemy()

def create_app():
    """
    Função fábrica para criar e configurar a aplicação Flask.
    Este padrão permite:
    - Criar múltiplas instâncias da aplicação
    - Configurar a aplicação de forma flexível
    - Facilitar testes com diferentes configurações
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
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
    # Organiza as rotas em módulos separados
    from app.routes import drivers, trucks, assignments
    app.register_blueprint(drivers.drivers_bp)
    app.register_blueprint(trucks.trucks_bp)
    app.register_blueprint(assignments.assignments_bp)
    
    # Criação das tabelas no banco de dados
    with app.app_context():
        db.create_all()
    
    # Configuração para aceitar rotas com ou sem barra no final
    app.url_map.strict_slashes = False
    
    return app 