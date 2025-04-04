from app import db

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    # Salva a data no formato YYYY-MM-DD
    date = db.Column(db.String(10), nullable=False)

    driver = db.relationship('Driver', backref=db.backref('assignments', cascade="all, delete-orphan"))
    truck = db.relationship('Truck', backref=db.backref('assignments', cascade="all, delete-orphan"))

    def to_dict(self):
        return {
            "id": self.id,
            "driver": self.driver.to_dict(),
            "truck": self.truck.to_dict(),
            "date": self.date,
        } 