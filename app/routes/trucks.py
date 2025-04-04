from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Truck
from app.utils.helpers import LICENSE_ORDER, validate_assignments

# Blueprint para agrupar todas as rotas relacionadas a caminhões
trucks_bp = Blueprint('trucks', __name__, url_prefix='/trucks')

@trucks_bp.route('/', methods=['GET'])
def get_trucks():
    # Lista todos os caminhões cadastrados.
    current_app.logger.info("Fetching all trucks")
    try:
        trucks = Truck.query.all()
        current_app.logger.info('Caminhões recuperados com sucesso')
        return jsonify([truck.to_dict() for truck in trucks]), 200
    except Exception as e:
        current_app.logger.error(f'Erro ao recuperar caminhões: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500

@trucks_bp.route('/<int:truck_id>', methods=['GET'])
def get_truck(truck_id):
    # Recupera os dados de um caminhão específico.
    current_app.logger.info(f"Fetching truck with ID {truck_id}")
    try:
        truck = Truck.query.get_or_404(truck_id)
        current_app.logger.info(f'Caminhão {truck_id} recuperado com sucesso')
        return jsonify(truck.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f'Erro ao recuperar caminhão {truck_id}: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500

@trucks_bp.route('/', methods=['POST'])
def create_truck():
    # Cria um novo caminhão.
    data = request.get_json()
    plate = data.get("plate")
    min_license_type = data.get("min_license_type")

    if not plate or not min_license_type or min_license_type not in LICENSE_ORDER:
        current_app.logger.error("Invalid data for the truck")
        return jsonify({"error": "Invalid data for the truck"}), 400

    # Valida se a placa já existe
    existing_truck = Truck.query.filter_by(plate=plate).first()
    if existing_truck:
        current_app.logger.error("A truck with this plate already exists")
        return jsonify({"error": "A truck with this plate already exists"}), 400

    truck = Truck(plate=plate, min_license_type=min_license_type)
    db.session.add(truck)
    db.session.commit()
    current_app.logger.info(f"Truck created with ID {truck.id}")
    return jsonify(truck.to_dict()), 201

@trucks_bp.route('/<int:truck_id>', methods=['PUT'])
def update_truck(truck_id):
    # Atualiza os dados de um caminhão existente.
    
    current_app.logger.info(f"Updating truck with ID {truck_id}")
    truck = Truck.query.get_or_404(truck_id)
    data = request.get_json()
    plate = data.get("plate")
    min_license_type = data.get("min_license_type")

    if plate:
        # Valida se a placa já existe
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

    # Valida as atribuições após a atualização do caminhão
    valid, message = validate_assignments()
    if not valid:
        db.session.rollback()
        current_app.logger.error(f"Assignment validation failed: {message}")
        return jsonify({"error": message}), 400

    current_app.logger.info(f"Truck with ID {truck.id} updated successfully")
    return jsonify(truck.to_dict())

@trucks_bp.route('/<int:truck_id>', methods=['DELETE'])
def delete_truck(truck_id):
    # Remove um caminhão do sistema.
    current_app.logger.info(f"Deleting truck with ID {truck_id}")
    truck = Truck.query.get_or_404(truck_id)
    db.session.delete(truck)
    db.session.commit()
    current_app.logger.info(f"Truck with ID {truck_id} deleted successfully")
    return jsonify({"message": "Truck successfully deleted."}) 