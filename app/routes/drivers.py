from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Driver
from app.utils.helpers import LICENSE_ORDER, validate_assignments

bp = Blueprint('drivers', __name__, url_prefix='/drivers')

@bp.route('/', methods=['GET'])
def get_drivers():
    current_app.logger.info("Fetching all drivers")
    drivers = Driver.query.all()
    return jsonify([driver.to_dict() for driver in drivers])

@bp.route('/<int:driver_id>', methods=['GET'])
def get_driver(driver_id):
    current_app.logger.info(f"Fetching driver with ID {driver_id}")
    driver = Driver.query.get_or_404(driver_id)
    return jsonify(driver.to_dict())

@bp.route('/', methods=['POST'])
def create_driver():
    data = request.get_json()
    name = data.get("name")
    license_type = data.get("license_type")

    if not name or not license_type or license_type not in LICENSE_ORDER:
        current_app.logger.error("Invalid data for the driver")
        return jsonify({"error": "Invalid data for the driver"}), 400

    driver = Driver(name=name, license_type=license_type)
    db.session.add(driver)
    db.session.commit()
    current_app.logger.info(f"Driver created with ID {driver.id}")
    return jsonify(driver.to_dict()), 201

@bp.route('/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    current_app.logger.info(f"Updating driver with ID {driver_id}")
    driver = Driver.query.get_or_404(driver_id)
    data = request.get_json()
    name = data.get("name")
    license_type = data.get("license_type")

    if name:
        driver.name = name
    if license_type:
        if license_type not in LICENSE_ORDER:
            current_app.logger.error("Invalid license type")
            return jsonify({"error": "Invalid license type"}), 400
        driver.license_type = license_type

    db.session.commit()

    # Validate assignments after updating driver
    valid, message = validate_assignments()
    if not valid:
        db.session.rollback()
        current_app.logger.error(f"Assignment validation failed: {message}")
        return jsonify({"error": message}), 400

    current_app.logger.info(f"Driver with ID {driver.id} updated successfully")
    return jsonify(driver.to_dict())

@bp.route('/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    current_app.logger.info(f"Deleting driver with ID {driver_id}")
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    current_app.logger.info(f"Driver with ID {driver_id} deleted successfully")
    return jsonify({"message": "Driver successfully deleted."}) 