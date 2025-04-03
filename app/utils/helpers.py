from datetime import datetime
from app import db
from app.models import Driver, Truck, Assignment

# Mapeamento dos níveis de carteira para comparação
# Usa valores numéricos para facilitar a comparação de níveis
LICENSE_ORDER = {
    "A": 1,  # Carteira mais básica
    "B": 2,  # Veículos de passeio
    "C": 3,  # Veículos de carga leve
    "D": 4,  # Veículos de carga pesada
    "E": 5,  # Veículos especiais
}

def is_license_valid(driver_license, truck_min_license):
    """
    Verifica se a carteira do motorista é compatível com o caminhão.
    
    Args:
        driver_license (str): Tipo da carteira do motorista (A-E)
        truck_min_license (str): Tipo mínimo de carteira exigido pelo caminhão (A-E)
    
    Returns:
        bool: True se a carteira for compatível, False caso contrário
    
    Exemplo:
        >>> is_license_valid("E", "D")
        True
        >>> is_license_valid("B", "E")
        False
    """
    return LICENSE_ORDER.get(driver_license, 0) >= LICENSE_ORDER.get(truck_min_license, 0)

def parse_date(date_str):
    """
    Valida se uma string está no formato de data correto (YYYY-MM-DD).
    
    Args:
        date_str (str): String contendo a data a ser validada
    
    Returns:
        bool: True se a data for válida, False caso contrário
    
    Exemplo:
        >>> parse_date("2024-04-03")
        True
        >>> parse_date("03-04-2024")
        False
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_assignments():
    """
    Valida todas as atribuições existentes no banco de dados.
    Verifica se todas as atribuições atendem às regras de negócio.
    
    Returns:
        tuple: (bool, str) - (True se todas as atribuições forem válidas, 
                             mensagem de erro se encontrar uma atribuição inválida)
    
    Exemplo:
        >>> validate_assignments()
        (True, "")
        >>> validate_assignments()
        (False, "Assignment ID 1 is invalid due to license incompatibility.")
    """
    assignments = Assignment.query.all()
    for assignment in assignments:
        if not is_license_valid(assignment.driver.license_type, assignment.truck.min_license_type):
            return False, f"Assignment ID {assignment.id} is invalid due to license incompatibility."
    return True, "" 