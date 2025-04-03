import os

class Config:
    # Configuração do SQLite para fins de exemplo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crud.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao' 