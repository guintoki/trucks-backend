from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Driver
from app.utils.helpers import LICENSE_ORDER, validate_assignments

# Blueprint para agrupar todas as rotas relacionadas a motoristas
drivers_bp = Blueprint('drivers', __name__, url_prefix='/drivers')

@drivers_bp.route('/', methods=['GET'])
def get_drivers():
    # Lista todos os motoristas cadastrados.
    try:
        current_app.logger.info("Fetching all drivers")
        drivers = Driver.query.all()
        current_app.logger.info('Motoristas recuperados com sucesso')
        return jsonify([driver.to_dict() for driver in drivers]), 200
    except Exception as e:
        current_app.logger.error(f'Erro ao recuperar motoristas: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500

@drivers_bp.route('/<int:driver_id>', methods=['GET'])
def get_driver(driver_id):
    # Recupera os dados de um motorista específico.
    try:
        current_app.logger.info(f"Fetching driver with ID {driver_id}")
        driver = Driver.query.get_or_404(driver_id)
        current_app.logger.info(f'Motorista {driver_id} recuperado com sucesso')
        return jsonify(driver.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f'Erro ao recuperar motorista {driver_id}: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500

@drivers_bp.route('/', methods=['POST'])
def create_driver():
    # Cria um novo motorista.
    try:
        data = request.get_json()
        
        # Validação dos dados obrigatórios
        if not data or 'name' not in data or 'license_type' not in data:
            current_app.logger.error("Invalid data for the driver")
            return jsonify({'error': 'Nome e tipo de carteira são obrigatórios'}), 400
            
        # Validação do tipo de carteira
        if data['license_type'] not in LICENSE_ORDER:
            current_app.logger.error("Invalid license type")
            return jsonify({'error': 'Tipo de carteira inválido'}), 400
            
        driver = Driver(
            name=data['name'],
            license_type=data['license_type']
        )
        
        db.session.add(driver)
        db.session.commit()
        
        current_app.logger.info(f"Driver created with ID {driver.id}")
        return jsonify(driver.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro ao criar motorista: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500

@drivers_bp.route('/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    # Atualiza os dados de um motorista existente.
    try:
        current_app.logger.info(f"Updating driver with ID {driver_id}")
        driver = Driver.query.get_or_404(driver_id)
        data = request.get_json()
        
        if 'name' in data:
            driver.name = data['name']
            
        if 'license_type' in data:
            if data['license_type'] not in LICENSE_ORDER:
                current_app.logger.error("Invalid license type")
                return jsonify({"error": "Invalid license type"}), 400
            driver.license_type = data['license_type']
            
        db.session.commit()
        
        # Validate assignments after updating driver
        valid, message = validate_assignments()
        if not valid:
            db.session.rollback()
            current_app.logger.error(f"Assignment validation failed: {message}")
            return jsonify({"error": message}), 400

        current_app.logger.info(f"Driver with ID {driver.id} updated successfully")
        return jsonify(driver.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro ao atualizar motorista {driver_id}: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500

@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    # Remove um motorista do sistema.
    try:
        current_app.logger.info(f"Deleting driver with ID {driver_id}")
        driver = Driver.query.get_or_404(driver_id)
        db.session.delete(driver)
        db.session.commit()
        
        current_app.logger.info(f"Driver with ID {driver_id} deleted successfully")
        return jsonify({"message": "Driver successfully deleted."}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro ao remover motorista {driver_id}: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor'}), 500 