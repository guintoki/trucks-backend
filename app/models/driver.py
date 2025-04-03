from app import db

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_type = db.Column(db.String(1), nullable=False)  # A, B, C, D or E

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "license_type": self.license_type,
        } 