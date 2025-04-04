from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Driver, Truck, Assignment
from app.utils.helpers import is_license_valid, parse_date

# Blueprint para agrupar todas as rotas relacionadas a atribuições
# Facilita a organização e manutenção do código
assignments_bp = Blueprint('assignments', __name__, url_prefix='/assignments')

@assignments_bp.route('/', methods=['GET'])
def get_assignments():
    # Lista todas as atribuições cadastradas.
    current_app.logger.info("Fetching all assignments")
    assignments = Assignment.query.all()
    return jsonify([assignment.to_dict() for assignment in assignments]), 200

@assignments_bp.route('/<int:assignment_id>', methods=['GET'])
def get_assignment(assignment_id):
    # Recupera os dados de uma atribuição específica.
    current_app.logger.info(f"Fetching assignment with ID {assignment_id}")
    assignment = Assignment.query.get_or_404(assignment_id)
    return jsonify(assignment.to_dict()), 200

@assignments_bp.route('/', methods=['POST'])
def create_assignment():
    # Cria uma nova atribuição.
    data = request.get_json()
    driver_id = data.get("driver_id")
    truck_id = data.get("truck_id")
    date_str = data.get("date")  # Formato esperado "YYYY-MM-DD"

    if not driver_id or not truck_id or not date_str:
        current_app.logger.error("driver_id, truck_id and date are required")
        return jsonify({"error": "driver_id, truck_id and date are required"}), 400

    if not parse_date(date_str):
        current_app.logger.error("Invalid date format. Use YYYY-MM-DD")
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    driver = Driver.query.get(driver_id)
    truck = Truck.query.get(truck_id)

    if not driver or not truck:
        current_app.logger.error("Driver or Truck not found")
        return jsonify({"error": "Driver or Truck not found"}), 404

    # Validação: O motorista não pode ter outra atribuição no mesmo dia
    driver_assignment = Assignment.query.filter_by(driver_id=driver_id, date=date_str).first()
    if driver_assignment:
        current_app.logger.error("The driver is already assigned to a truck on this date")
        return jsonify({"error": "The driver is already assigned to a truck on this date"}), 400

    # Validação: O caminhão não pode ter outra atribuição no mesmo dia
    truck_assignment = Assignment.query.filter_by(truck_id=truck_id, date=date_str).first()
    if truck_assignment:
        current_app.logger.error("The truck is already assigned to a driver on this date")
        return jsonify({"error": "The truck is already assigned to a driver on this date"}), 400

    # Validação: Verifica se a carteira do motorista é compatível com o caminhão
    if not is_license_valid(driver.license_type, truck.min_license_type):
        current_app.logger.error("The driver's license type is not compatible with the truck")
        return jsonify({"error": "The driver's license type is not compatible with the truck"}), 400

    assignment = Assignment(driver_id=driver_id, truck_id=truck_id, date=date_str)
    db.session.add(assignment)
    db.session.commit()
    current_app.logger.info(f"Assignment created with ID {assignment.id}")
    return jsonify(assignment.to_dict()), 201

@assignments_bp.route('/<int:assignment_id>', methods=['PUT'])
def update_assignment(assignment_id):
    # Atualiza os dados de uma atribuição existente.
    current_app.logger.info(f"Updating assignment with ID {assignment_id}")
    assignment = Assignment.query.get_or_404(assignment_id)
    data = request.get_json()
    driver_id = data.get("driver_id", assignment.driver_id)
    truck_id = data.get("truck_id", assignment.truck_id)
    date_str = data.get("date", assignment.date)

    if not parse_date(date_str):
        current_app.logger.error("Invalid date format. Use YYYY-MM-DD")
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    driver = Driver.query.get(driver_id)
    truck = Truck.query.get(truck_id)
    if not driver or not truck:
        current_app.logger.error("Driver or Truck not found")
        return jsonify({"error": "Driver or Truck not found"}), 404

    # Validação: se houver mudança de motorista ou data, verifica se o motorista já tem uma atribuição nesse dia
    if (driver_id != assignment.driver_id or date_str != assignment.date):
        driver_assignment = Assignment.query.filter_by(driver_id=driver_id, date=date_str).first()
        if driver_assignment and driver_assignment.id != assignment.id:
            current_app.logger.error("The driver is already assigned to a truck on this date")
            return jsonify({"error": "The driver is already assigned to a truck on this date"}), 400

    # Validaçao: se houver mudança de caminhão ou data, verifica se o caminhão já tem uma atribuição nesse dia
    if (truck_id != assignment.truck_id or date_str != assignment.date):
        truck_assignment = Assignment.query.filter_by(truck_id=truck_id, date=date_str).first()
        if truck_assignment and truck_assignment.id != assignment.id:
            current_app.logger.error("The truck is already assigned to a driver on this date")
            return jsonify({"error": "The truck is already assigned to a driver on this date"}), 400

    # Validação: Verifica se a carteira do motorista é compatível com o caminhão
    if not is_license_valid(driver.license_type, truck.min_license_type):
        current_app.logger.error("The driver's license type is not compatible with the truck")
        return jsonify({"error": "The driver's license type is not compatible with the truck"}), 400

    assignment.driver_id = driver_id
    assignment.truck_id = truck_id
    assignment.date = date_str

    db.session.commit()
    current_app.logger.info(f"Assignment with ID {assignment.id} updated successfully")
    return jsonify(assignment.to_dict())

@assignments_bp.route('/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    # Remove uma atribuição do sistema.
    current_app.logger.info(f"Deleting assignment with ID {assignment_id}")
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    current_app.logger.info(f"Assignment with ID {assignment_id} deleted successfully")
    return jsonify({"message": "Assignment successfully deleted."}) 