# IDS706_Final Project Alejandro Paredes La Torre, Alex Ackerman, Christian Moreira

# Movie Database Project with Flask and Airflow

This project sets up a Movie Database API using Flask as the backend and Apache Airflow for workflow orchestration. The system leverages Docker for containerized deployments and PostgreSQL as the database.

## Prerequisites

Before running the project, ensure you have the following installed:
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)

## Project Structure
```
.
├── backend/
│   ├── app.py               # Flask application
│   ├── templates/           # HTML templates for the web app
│   ├── data/
│       ├── db_connection.py # Database connection module
├── airflow/
│   ├── dags/                # Airflow DAGs
│   ├── logs/                # Airflow logs
│   ├── plugins/             # Airflow plugins
├── docker-compose.yml       # Docker Compose configuration
├── .env                     # Environment variables for the project
```

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a `.env` file in the root directory with the following contents:
   ```
   FLASK_RUN_HOST=0.0.0.0
   FLASK_APP=app.py
   FLASK_ENV=development
   AIRFLOW_UID=50000
   _AIRFLOW_WWW_USER_USERNAME=airflow
   _AIRFLOW_WWW_USER_PASSWORD=airflow
   ACCESS_TOKEN=#databricks access token
   SERVER_HOSTNAME=#databricks server
   DWH_DB=#databricks db
   LLM_API_KEY=#Create a user account in Gemini for their API 
   ```

3. Start the project using Docker Compose:
   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the Flask backend (`flask-app`) and Airflow components.
   - Start all services, including:
     - Flask app (accessible on [http://localhost:5000](http://localhost:5000))
     - Airflow webserver (accessible on [http://localhost:8080](http://localhost:8080))
     - PostgreSQL database

4. Access the services:
   - Flask API: [http://localhost:5000](http://localhost:5000)
   - Airflow Dashboard: [http://localhost:8080](http://localhost:8080)
     - Username: `airflow`
     - Password: `airflow`

## Flask Backend Features

- **Home Page**: Displays the main page (`/`).
- **Search Movies**: Search movies by name or genre (`/movies`, `/movies/<genre>`).
- **Individual Movie**: Fetch details for a specific movie by ID (`/movie/<id>`).

## Airflow Features

- **DAGs Folder**: Place your custom DAGs in the `airflow/dags` directory.
- **Monitoring**: View and monitor DAG execution via the Airflow UI.
- **Scheduler**: Automates task execution.

## Database Configuration

The PostgreSQL database is configured as follows:
- **User**: `airflow`
- **Password**: `airflow`
- **Database Name**: `airflow`
- **Host**: `postgres`

You can modify the database credentials in `docker-compose.yml` if needed.

## Logs and Debugging

- Flask logs are stored in `backend/app.log`.
- Airflow logs are stored in `airflow/logs`.

## Stopping the Services

To stop the services, run:
```bash
docker-compose down
```

To remove all containers, volumes, and networks:
```bash
docker-compose down --volumes --remove-orphans
```

---

For further questions or issues, feel free to open a discussion or raise an issue in the repository!