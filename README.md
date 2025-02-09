# CRUD Drivers and Trucks

This project is a backend CRUD for managing drivers, trucks, and assignments using Flask.

## Requirements

- Python 3.6+
- Pip

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/crud_drivers_trucks.git
   cd crud_drivers_trucks
   ```

2. Create a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Running the Project

1. Start the Flask server:

   ```sh
   python app.py
   ```

2. The server will be running at `http://localhost:5000`.

## Endpoints

### Drivers

- `GET /drivers` - Returns all drivers.
- `GET /drivers/<int:driver_id>` - Returns a specific driver.
- `POST /drivers` - Creates a new driver.
- `PUT /drivers/<int:driver_id>` - Updates an existing driver.
- `DELETE /drivers/<int:driver_id>` - Deletes a driver.

### Trucks

- `GET /trucks` - Returns all trucks.
- `GET /trucks/<int:truck_id>` - Returns a specific truck.
- `POST /trucks` - Creates a new truck.
- `PUT /trucks/<int:truck_id>` - Updates an existing truck.
- `DELETE /trucks/<int:truck_id>` - Deletes a truck.

### Assignments

- `GET /assignments` - Returns all assignments.
- `GET /assignments/<int:assignment_id>` - Returns a specific assignment.
- `POST /assignments` - Creates a new assignment.
- `PUT /assignments/<int:assignment_id>` - Updates an existing assignment.
- `DELETE /assignments/<int:assignment_id>` - Deletes an assignment.
