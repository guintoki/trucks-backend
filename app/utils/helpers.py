from datetime import datetime
from app import db
from app.models import Driver, Truck, Assignment

# Mapping license levels for easier comparison
LICENSE_ORDER = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
}

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