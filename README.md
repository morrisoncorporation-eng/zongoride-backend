# ZongoRide Fleet Management API

This is the back-end API for the ZongoRide fleet management system. It is built with Python and the Django framework and provides a RESTful API for managing scooters and bikes.

## Features

- **Scooter Management:** Create, retrieve, update, and delete scooters.
- **Bike Management:** Create, retrieve, update, and delete bikes.
- **Remote Lock/Unlock:** Lock and unlock scooters remotely.
- **Real-time IoT Updates:** An MQTT listener is included to receive real-time location and status updates from IoT devices on the scooters.
- **Modern Admin UI:** A customized admin dashboard using `django-jazzmin` for a better user experience.

## Architecture

The ZongoRide backend is designed with a modular architecture that separates the core API from the real-time IoT data processing.

-   **Django REST API:** The heart of the system, built with Django and the Django REST Framework. It exposes a set of RESTful endpoints for the mobile app to consume. All business logic for managing scooters and bikes is handled here.

-   **IoT Devices (Scooters):** Each scooter is equipped with an IoT device that sends data (location, status, battery level) to an MQTT broker.

-   **MQTT Broker:** A central message broker that receives data from all IoT devices. This decouples the IoT devices from the backend API.

-   **MQTT Listener:** A Django management command (`mqtt_listener`) that runs as a separate process. It connects to the MQTT broker, subscribes to the relevant topics, and updates the database in real-time as new data arrives from the scooters.

-   **Database:** A PostgreSQL or SQLite database that stores all the data for the scooters, bikes, user accounts, and other system information.

-   **Mobile App:** The front-end mobile application (iOS/Android) that communicates with the Django REST API to allow users to find, unlock, and manage scooters.

Here is a simplified diagram of the data flow:

```
+----------------+      +------------------+      +-----------------+
|                |      |                  |      |                 |
|  Mobile App    +----->|  Django REST API +----->|    Database     |
|                |      |                  |      |                 |
+----------------+      +------------------+      +-------^---------+
                                                          |
                                                          | (Updates)
                                                          |
+----------------+      +------------------+      +-------+---------+
|                |      |                  |      |                 |
|  IoT Devices   +----->|   MQTT Broker    +----->|  MQTT Listener  |
| (Scooters)     |      |                  |      | (Django Command)|
|                |      |                  |      |                 |
+----------------+      +------------------+      +-----------------+
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3
- Pip
- Virtualenv

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r mysite/requirements.txt
    ```

4.  **Run the database migrations:**

    ```bash
    python mysite/manage.py migrate
    ```

5.  **Create a superuser to access the admin dashboard:**

    ```bash
    python mysite/manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    ./devserver.sh
    ```

The API will be available at `http://127.0.0.1:8000/`.

## API Authentication

The API uses token-based authentication with `djangorestframework-simplejwt`. To access the protected endpoints, you must include a valid JSON Web Token (JWT) in the `Authorization` header of your requests.

### 1. Get an Authentication Token

To get a token, make a `POST` request to the `/api/token/` endpoint with your username and password.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' http://127.0.0.1:8000/api/token/
```

The response will contain an access and refresh token:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Access Protected Endpoints

To access a protected endpoint, include the `access` token in the `Authorization` header as a "Bearer" token.

```bash
curl -H "Authorization: Bearer <your_access_token>" http://127.0.0.1:8000/api/scooters/
```

## API Endpoints

### Scooters

- `GET /scooters/`: Retrieve a list of all scooters.
- `POST /scooters/`: Create a new scooter.
- `GET /scooters/<id>/`: Retrieve a specific scooter.
- `PUT /scooters/<id>/`: Update a specific scooter.
- `DELETE /scooters/<id>/`: Delete a specific scooter.
- `POST /scooters/<id>/lock/`: Lock a specific scooter.
- `POST /scooters/<id>/unlock/`: Unlock a specific scooter.

### Bikes

- `GET /bikes/`: Retrieve a list of all bikes.
- `POST /bikes/`: Create a new bike.
- `GET /bikes/<id>/`: Retrieve a specific bike.
- `PUT /bikes/<id>/`: Update a specific bike.
- `DELETE /bikes/<id>/`: Delete a specific bike.

## MQTT Listener

To receive real-time updates from IoT devices, run the MQTT listener:

```bash
python mysite/manage.py mqtt_listener
```

This command starts a client that subscribes to the following topics:

- `scooters/+/location`: For scooter location updates.
- `scooters/+/status`: For scooter status and battery level updates.

**Note:** You will need to configure the MQTT broker address in `mysite/fleet/management/commands/mqtt_listener.py`.

## Admin Dashboard

Access the admin dashboard at `/admin/`. The UI is customized with `django-jazzmin` for a modern look and feel.
