import os

class Config:
    """
    Classe de configuração base da aplicação.
    Segue o padrão de configuração do Flask, permitindo:
    - Configurações diferentes para diferentes ambientes
    - Uso de variáveis de ambiente para valores sensíveis
    - Fácil extensão para outras configurações
    """
    # Configuração do SQLite para desenvolvimento
    # Em produção, considere usar PostgreSQL ou outro banco de dados mais robusto
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crud.db'
    
    # Desativa o rastreamento de modificações do SQLAlchemy
    # Melhora a performance e reduz o uso de memória
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Chave secreta para sessões e tokens
    # Em produção, use uma chave forte e mantenha-a em variável de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao' 