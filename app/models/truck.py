from app import db

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), nullable=False, unique=True)
    min_license_type = db.Column(db.String(1), nullable=False)  # A, B, C, D or E

    def to_dict(self):
        return {
            "id": self.id,
            "plate": self.plate,
            "min_license_type": self.min_license_type,
        } 