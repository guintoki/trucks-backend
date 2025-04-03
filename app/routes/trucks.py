from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Truck
from app.utils.helpers import LICENSE_ORDER, validate_assignments

bp = Blueprint('trucks', __name__, url_prefix='/trucks')

@bp.route('/', methods=['GET'])
def get_trucks():
    current_app.logger.info("Fetching all trucks")
    trucks = Truck.query.all()
    return jsonify([truck.to_dict() for truck in trucks])

@bp.route('/<int:truck_id>', methods=['GET'])
def get_truck(truck_id):
    current_app.logger.info(f"Fetching truck with ID {truck_id}")
    truck = Truck.query.get_or_404(truck_id)
    return jsonify(truck.to_dict())

@bp.route('/', methods=['POST'])
def create_truck():
    data = request.get_json()
    plate = data.get("plate")
    min_license_type = data.get("min_license_type")

    if not plate or not min_license_type or min_license_type not in LICENSE_ORDER:
        current_app.logger.error("Invalid data for the truck")
        return jsonify({"error": "Invalid data for the truck"}), 400

    # Check if a truck with the same plate already exists
    existing_truck = Truck.query.filter_by(plate=plate).first()
    if existing_truck:
        current_app.logger.error("A truck with this plate already exists")
        return jsonify({"error": "A truck with this plate already exists"}), 400

    truck = Truck(plate=plate, min_license_type=min_license_type)
    db.session.add(truck)
    db.session.commit()
    current_app.logger.info(f"Truck created with ID {truck.id}")
    return jsonify(truck.to_dict()), 201

@bp.route('/<int:truck_id>', methods=['PUT'])
def update_truck(truck_id):
    current_app.logger.info(f"Updating truck with ID {truck_id}")
    truck = Truck.query.get_or_404(truck_id)
    data = request.get_json()
    plate = data.get("plate")
    min_license_type = data.get("min_license_type")

    if plate:
        # Check if a truck with the same plate already exists
        existing_truck = Truck.query.filter_by(plate=plate).first()
        if existing_truck and existing_truck.id != truck_id:
            current_app.logger.error("A truck with this plate already exists")
            return jsonify({"error": "A truck with this plate already exists"}), 400
        truck.plate = plate
    if min_license_type:
        if min_license_type not in LICENSE_ORDER:
            current_app.logger.error("Invalid min_license_type")
            return jsonify({"error": "Invalid min_license_type"}), 400
        truck.min_license_type = min_license_type

    db.session.commit()

    # Validate assignments after updating truck
    valid, message = validate_assignments()
    if not valid:
        db.session.rollback()
        current_app.logger.error(f"Assignment validation failed: {message}")
        return jsonify({"error": message}), 400

    current_app.logger.info(f"Truck with ID {truck.id} updated successfully")
    return jsonify(truck.to_dict())

@bp.route('/<int:truck_id>', methods=['DELETE'])
def delete_truck(truck_id):
    current_app.logger.info(f"Deleting truck with ID {truck_id}")
    truck = Truck.query.get_or_404(truck_id)
    db.session.delete(truck)
    db.session.commit()
    current_app.logger.info(f"Truck with ID {truck_id} deleted successfully")
    return jsonify({"message": "Truck successfully deleted."}) 