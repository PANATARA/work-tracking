# Project Management System

## Installation Instructions

To set up the backend application using `docker-compose`, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/PANATARA/work-tracking.git
    cd work-tracking
    ```

2. **Create a `.env` file**:

    Modify the `.env` file with your specific configuration.

3. **Build and start the containers**:
    ```sh
    docker-compose up --build
    ```

4. **Access the Django shell**:
    ```sh
    docker-compose exec django bash
    ```

5. **Apply database migrations**:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

7. **Exit the Django shell**:
    ```sh
    exit
    ```

8. **Access the application**:
    Open your browser and navigate to `http://localhost:8000` (or the port specified in your `docker-compose.yml`).

9. **Stop the containers**:
    ```sh
    docker-compose down
    ```
