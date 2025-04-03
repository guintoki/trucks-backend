from app import db
from datetime import datetime

class Driver(db.Model):
    """
    Modelo que representa um motorista no sistema.
    
    Attributes:
        id (int): Identificador único do motorista
        name (str): Nome completo do motorista
        license_type (str): Tipo da carteira de motorista (A-E)
        assignments (relationship): Relacionamento com as atribuições do motorista
        created_at (datetime): Data de criação do registro
        updated_at (datetime): Data da última atualização
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_type = db.Column(db.String(1), nullable=False)
    assignments = db.relationship('Assignment', backref='driver', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        Converte o objeto Driver para um dicionário.
        
        Returns:
            dict: Representação do motorista em formato JSON
        """
        return {
            'id': self.id,
            'name': self.name,
            'license_type': self.license_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Truck(db.Model):
    """
    Modelo que representa um caminhão no sistema.
    
    Attributes:
        id (int): Identificador único do caminhão
        model (str): Modelo do caminhão
        plate (str): Placa do caminhão
        min_license_type (str): Tipo mínimo de carteira necessária (A-E)
        assignments (relationship): Relacionamento com as atribuições do caminhão
        created_at (datetime): Data de criação do registro
        updated_at (datetime): Data da última atualização
    """
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    plate = db.Column(db.String(7), nullable=False, unique=True)
    min_license_type = db.Column(db.String(1), nullable=False)
    assignments = db.relationship('Assignment', backref='truck', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        Converte o objeto Truck para um dicionário.
        
        Returns:
            dict: Representação do caminhão em formato JSON
        """
        return {
            'id': self.id,
            'model': self.model,
            'plate': self.plate,
            'min_license_type': self.min_license_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Assignment(db.Model):
    """
    Modelo que representa uma atribuição de motorista a um caminhão.
    
    Attributes:
        id (int): Identificador único da atribuição
        driver_id (int): ID do motorista atribuído
        truck_id (int): ID do caminhão atribuído
        start_date (date): Data de início da atribuição
        end_date (date): Data de término da atribuição
        created_at (datetime): Data de criação do registro
        updated_at (datetime): Data da última atualização
    """
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        Converte o objeto Assignment para um dicionário.
        
        Returns:
            dict: Representação da atribuição em formato JSON
        """
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'truck_id': self.truck_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 