# ZongoRide Fleet Management API

This is the back-end API for the ZongoRide fleet management system. It is built with Python and the Django framework and provides a RESTful API for managing scooters and bikes.

## Features

- **Geospatial Data:** Utilizes PostGIS to store and query location data for all fleet vehicles.
- **Scooter & Bike Management:** Full CRUD (Create, Retrieve, Update, Delete) operations for scooters and bikes.
- **Remote Lock/Unlock:** Lock and unlock scooters remotely.
- **Real-time IoT Updates:** An MQTT listener is included to receive real-time location and status updates from IoT devices on the scooters.
- **Modern Admin UI:** A customized admin dashboard using `django-jazzmin` for a better user experience.

## Architecture

The ZongoRide backend is designed with a modular, containerized architecture that separates the core API from real-time data processing and other services.

```mermaid
graph TD
    subgraph "User Interaction"
        A[Admin/Operator] --> B{Django Admin UI};
        C[Rider App] --> D{REST API};
    end

    subgraph "ZongoRide Backend (Docker Compose)"
        B --> E[Web App (Django/Gunicorn)];
        D --> E;
        E -- CRUD Ops --> F[(PostgreSQL/PostGIS DB)];
        G[IoT Devices] -- MQTT pub --> H{MQTT Broker};
        I[MQTT Listener] -- MQTT sub --> H;
        I -- Updates --> E;
    end

    style F fill:#d9e6f3,stroke:#333,stroke-width:2px
    style H fill:#d9f3e6,stroke:#333,stroke-width:2px
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes using Docker.

### Prerequisites

- **Docker:** [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose:** [Install Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/zongoride-backend.git
    cd zongoride-backend
    ```

2.  **Create an Environment File:**

    The application uses environment variables for configuration. Create a file named `.env` in the project root. Copy the contents of `.env.example` into it. This file is used by `docker-compose` to configure the database connection.

    ```bash
    cp .env.example .env
    ```

3.  **Build and Start the Containers:**

    This command will build the Docker image for the web application, start all services (web app, database, MQTT broker), and run them in the background.

    ```bash
    docker-compose up --build -d
    ```

4.  **Apply Database Migrations:**

    Once the containers are running, you need to apply the database migrations to set up the database schema.

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Create a Superuser:**

    To access the Django admin panel, you need to create an administrator account.

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    Follow the prompts to create your username, email, and password.

6.  **Access the Application:**

    You can now access the application:
    - **Admin Panel:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
    - **API Root:** [http://localhost:8000/api/](http://localhost:8000/api/)
    - **API Documentation (Swagger UI):** [http://localhost:8000/api/swagger/](http://localhost:8000/api/swagger/)
    - **API Documentation (ReDoc):** [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)


## API Usage

The API is built using Django REST Framework. You can interact with it using tools like `curl` or Postman. Authentication is handled via JWT.

- **`/api/token/`**: Obtain a JWT by POSTing username and password.
- **`/api/token/refresh/`**: Refresh an expired JWT.
- **`/api/fleet/scooters/`**: List or create scooters.

## Running Tests

To run the automated test suite, use the following command:

```bash
docker-compose exec web python manage.py test
```
