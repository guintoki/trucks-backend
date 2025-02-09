from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuring SQLite database for example purposes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Mapping license levels for easier comparison
LICENSE_ORDER = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
}

# MODELS
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

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    # We will store the date in the format YYYY-MM-DD
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

# Create tables
with app.app_context():
    db.create_all()

# HELPER FUNCTIONS

def is_license_valid(driver_license, truck_min_license):
    """
    Returns True if the driver's license level is sufficient to operate the truck.
    The comparison is made using the mapping defined in LICENSE_ORDER.
    """
    return LICENSE_ORDER.get(driver_license, 0) >= LICENSE_ORDER.get(truck_min_license, 0)

def parse_date(date_str):
    """
    Checks if the string is in the correct format (YYYY-MM-DD)
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_assignments():
    """
    Validates all assignments to ensure they meet the rules.
    """
    assignments = Assignment.query.all()
    for assignment in assignments:
        if not is_license_valid(assignment.driver.license_type, assignment.truck.min_license_type):
            return False, f"Assignment ID {assignment.id} is invalid due to license incompatibility."
    return True, ""

# ROUTES FOR DRIVERS

@app.route("/drivers", methods=["GET"])
def get_drivers():
    app.logger.info("Fetching all drivers")
    drivers = Driver.query.all()
    return jsonify([driver.to_dict() for driver in drivers])

@app.route("/drivers/<int:driver_id>", methods=["GET"])
def get_driver(driver_id):
    app.logger.info(f"Fetching driver with ID {driver_id}")
    driver = Driver.query.get_or_404(driver_id)
    return jsonify(driver.to_dict())

@app.route("/drivers", methods=["POST"])
def create_driver():
    data = request.get_json()
    name = data.get("name")
    license_type = data.get("license_type")

    if not name or not license_type or license_type not in LICENSE_ORDER:
        app.logger.error("Invalid data for the driver")
        return jsonify({"error": "Invalid data for the driver"}), 400

    driver = Driver(name=name, license_type=license_type)
    db.session.add(driver)
    db.session.commit()
    app.logger.info(f"Driver created with ID {driver.id}")
    return jsonify(driver.to_dict()), 201

@app.route("/drivers/<int:driver_id>", methods=["PUT"])
def update_driver(driver_id):
    app.logger.info(f"Updating driver with ID {driver_id}")
    driver = Driver.query.get_or_404(driver_id)
    data = request.get_json()
    name = data.get("name")
    license_type = data.get("license_type")

    if name:
        driver.name = name
    if license_type:
        if license_type not in LICENSE_ORDER:
            app.logger.error("Invalid license type")
            return jsonify({"error": "Invalid license type"}), 400
        driver.license_type = license_type

    db.session.commit()

    # Validate assignments after updating driver
    valid, message = validate_assignments()
    if not valid:
        db.session.rollback()
        app.logger.error(f"Assignment validation failed: {message}")
        return jsonify({"error": message}), 400

    app.logger.info(f"Driver with ID {driver.id} updated successfully")
    return jsonify(driver.to_dict())

@app.route("/drivers/<int:driver_id>", methods=["DELETE"])
def delete_driver(driver_id):
    app.logger.info(f"Deleting driver with ID {driver_id}")
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    app.logger.info(f"Driver with ID {driver_id} deleted successfully")
    return jsonify({"message": "Driver successfully deleted."})

# ROUTES FOR TRUCKS

@app.route("/trucks", methods=["GET"])
def get_trucks():
    app.logger.info("Fetching all trucks")
    trucks = Truck.query.all()
    return jsonify([truck.to_dict() for truck in trucks])

@app.route("/trucks/<int:truck_id>", methods=["GET"])
def get_truck(truck_id):
    app.logger.info(f"Fetching truck with ID {truck_id}")
    truck = Truck.query.get_or_404(truck_id)
    return jsonify(truck.to_dict())

@app.route("/trucks", methods=["POST"])
def create_truck():
    data = request.get_json()
    plate = data.get("plate")
    min_license_type = data.get("min_license_type")

    if not plate or not min_license_type or min_license_type not in LICENSE_ORDER:
        app.logger.error("Invalid data for the truck")
        return jsonify({"error": "Invalid data for the truck"}), 400

    # Check if a truck with the same plate already exists
    existing_truck = Truck.query.filter_by(plate=plate).first()
    if existing_truck:
        app.logger.error("A truck with this plate already exists")
        return jsonify({"error": "A truck with this plate already exists"}), 400

    truck = Truck(plate=plate, min_license_type=min_license_type)
    db.session.add(truck)
    db.session.commit()
    app.logger.info(f"Truck created with ID {truck.id}")
    return jsonify(truck.to_dict()), 201

@app.route("/trucks/<int:truck_id>", methods=["PUT"])
def update_truck(truck_id):
    app.logger.info(f"Updating truck with ID {truck_id}")
    truck = Truck.query.get_or_404(truck_id)
    data = request.get_json()
    plate = data.get("plate")
    min_license_type = data.get("min_license_type")

    if plate:
        # Check if a truck with the same plate already exists
        existing_truck = Truck.query.filter_by(plate=plate).first()
        if existing_truck and existing_truck.id != truck_id:
            app.logger.error("A truck with this plate already exists")
            return jsonify({"error": "A truck with this plate already exists"}), 400
        truck.plate = plate
    if min_license_type:
        if min_license_type not in LICENSE_ORDER:
            app.logger.error("Invalid min_license_type")
            return jsonify({"error": "Invalid min_license_type"}), 400
        truck.min_license_type = min_license_type

    db.session.commit()

    # Validate assignments after updating truck
    valid, message = validate_assignments()
    if not valid:
        db.session.rollback()
        app.logger.error(f"Assignment validation failed: {message}")
        return jsonify({"error": message}), 400

    app.logger.info(f"Truck with ID {truck.id} updated successfully")
    return jsonify(truck.to_dict())

@app.route("/trucks/<int:truck_id>", methods=["DELETE"])
def delete_truck(truck_id):
    app.logger.info(f"Deleting truck with ID {truck_id}")
    truck = Truck.query.get_or_404(truck_id)
    db.session.delete(truck)
    db.session.commit()
    app.logger.info(f"Truck with ID {truck_id} deleted successfully")
    return jsonify({"message": "Truck successfully deleted."})

# ROUTES FOR ASSIGNMENTS

@app.route("/assignments", methods=["GET"])
def get_assignments():
    app.logger.info("Fetching all assignments")
    assignments = Assignment.query.all()
    return jsonify([assignment.to_dict() for assignment in assignments])

@app.route("/assignments/<int:assignment_id>", methods=["GET"])
def get_assignment(assignment_id):
    app.logger.info(f"Fetching assignment with ID {assignment_id}")
    assignment = Assignment.query.get_or_404(assignment_id)
    return jsonify(assignment.to_dict())

@app.route("/assignments", methods=["POST"])
def create_assignment():
    data = request.get_json()
    driver_id = data.get("driver_id")
    truck_id = data.get("truck_id")
    date_str = data.get("date")  # Expects format "YYYY-MM-DD"

    if not driver_id or not truck_id or not date_str:
        app.logger.error("driver_id, truck_id and date are required")
        return jsonify({"error": "driver_id, truck_id and date are required"}), 400

    if not parse_date(date_str):
        app.logger.error("Invalid date format. Use YYYY-MM-DD")
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    driver = Driver.query.get(driver_id)
    truck = Truck.query.get(truck_id)

    if not driver or not truck:
        app.logger.error("Driver or Truck not found")
        return jsonify({"error": "Driver or Truck not found"}), 404

    # Validation: The driver cannot have another assignment on the same date
    driver_assignment = Assignment.query.filter_by(driver_id=driver_id, date=date_str).first()
    if driver_assignment:
        app.logger.error("The driver is already assigned to a truck on this date")
        return jsonify({"error": "The driver is already assigned to a truck on this date"}), 400

    # Validation: The truck cannot have another driver on the same date
    truck_assignment = Assignment.query.filter_by(truck_id=truck_id, date=date_str).first()
    if truck_assignment:
        app.logger.error("The truck is already assigned to a driver on this date")
        return jsonify({"error": "The truck is already assigned to a driver on this date"}), 400

    # Validation: The driver must have a license compatible with the truck
    if not is_license_valid(driver.license_type, truck.min_license_type):
        app.logger.error("The driver's license type is not compatible with the truck")
        return jsonify({"error": "The driver's license type is not compatible with the truck"}), 400

    assignment = Assignment(driver_id=driver_id, truck_id=truck_id, date=date_str)
    db.session.add(assignment)
    db.session.commit()
    app.logger.info(f"Assignment created with ID {assignment.id}")
    return jsonify(assignment.to_dict()), 201

@app.route("/assignments/<int:assignment_id>", methods=["PUT"])
def update_assignment(assignment_id):
    app.logger.info(f"Updating assignment with ID {assignment_id}")
    assignment = Assignment.query.get_or_404(assignment_id)
    data = request.get_json()
    driver_id = data.get("driver_id", assignment.driver_id)
    truck_id = data.get("truck_id", assignment.truck_id)
    date_str = data.get("date", assignment.date)

    if not parse_date(date_str):
        app.logger.error("Invalid date format. Use YYYY-MM-DD")
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    driver = Driver.query.get(driver_id)
    truck = Truck.query.get(truck_id)
    if not driver or not truck:
        app.logger.error("Driver or Truck not found")
        return jsonify({"error": "Driver or Truck not found"}), 404

    # Validation: if there is a change of driver or date, check if the driver already has an assignment on that date
    if (driver_id != assignment.driver_id or date_str != assignment.date):
        driver_assignment = Assignment.query.filter_by(driver_id=driver_id, date=date_str).first()
        if driver_assignment and driver_assignment.id != assignment.id:
            app.logger.error("The driver is already assigned to a truck on this date")
            return jsonify({"error": "The driver is already assigned to a truck on this date"}), 400

    # Validation: if there is a change of truck or date, check if the truck already has an assignment on that date
    if (truck_id != assignment.truck_id or date_str != assignment.date):
        truck_assignment = Assignment.query.filter_by(truck_id=truck_id, date=date_str).first()
        if truck_assignment and truck_assignment.id != assignment.id:
            app.logger.error("The truck is already assigned to a driver on this date")
            return jsonify({"error": "The truck is already assigned to a driver on this date"}), 400

    # Validation: check license compatibility
    if not is_license_valid(driver.license_type, truck.min_license_type):
        app.logger.error("The driver's license type is not compatible with the truck")
        return jsonify({"error": "The driver's license type is not compatible with the truck"}), 400

    assignment.driver_id = driver_id
    assignment.truck_id = truck_id
    assignment.date = date_str

    db.session.commit()
    app.logger.info(f"Assignment with ID {assignment.id} updated successfully")
    return jsonify(assignment.to_dict())

@app.route("/assignments/<int:assignment_id>", methods=["DELETE"])
def delete_assignment(assignment_id):
    app.logger.info(f"Deleting assignment with ID {assignment_id}")
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    app.logger.info(f"Assignment with ID {assignment_id} deleted successfully")
    return jsonify({"message": "Assignment successfully deleted."})

# Root route for testing
@app.route("/")
def index():
    return "Backend CRUD for Drivers, Trucks, and Assignments running!"

if __name__ == "__main__":
    app.run(debug=True)
