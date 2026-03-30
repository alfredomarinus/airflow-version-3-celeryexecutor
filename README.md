# Airflow 3 + CeleryExecutor

Apache Airflow 3 running on Docker Compose with the **CeleryExecutor** backend.

## Architecture

| Service | Description |
|---------|-------------|
| **airflow-api-server** | Web UI and REST API (port `8080`) |
| **airflow-scheduler** | Schedules DAG runs |
| **airflow-dag-processor** | Parses DAG files |
| **airflow-worker** | Celery worker that executes tasks |
| **airflow-triggerer** | Handles deferrable operators |
| **flower** | Celery task monitoring dashboard (port `5555`) |
| **postgres** | Metadata database |
| **redis** | Celery message broker |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) ≥ 24.0
- [Docker Compose](https://docs.docker.com/compose/install/) ≥ 2.20
- At least **8 GB RAM** allocated to Docker

## Quick Start

```bash
# 1. Clone the repository and navigate to it
git clone <repo-url> && cd airflow-version-3-celeryexecutor

# 2. Copy the example env file and edit as needed
cp .env.example .env

# 3. Generate required Airflow secret keys (required for security)
# Generate fernet key:
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" | xargs -I {} sed -i '' 's/AIRFLOW__CORE__FERNET_KEY=CHANGE_ME/AIRFLOW__CORE__FERNET_KEY={}/' .env

# 4. Build and start all services
make build && make up

# 5. Check the logs to ensure everything started properly
make logs
```

> **Note:** On first run, the `airflow-init` container will initialize the database and create directories. This may take 1-2 minutes. Wait for all services to show `healthy` status.

## Common Operations

```bash
make up              # Start services in background
make down            # Stop all running services
make restart         # Restart all running services
make logs            # Follow all service logs
make reset           # Stop everything, remove volumes, and restart fresh
make status          # Show running containers
make shell           # Open a bash shell in the API server
make build           # Rebuild images (after Dockerfile changes)
make clean           # Remove cache files and logs
```

## Project Structure

```
airflow-version-3-celeryexecutor/
├── airflow/
│   ├── config/
│   │   └── airflow.cfg          # Airflow configuration
│   ├── dags/                    # Place your DAG files here
│   │   └── hello_world.py       # Example DAG
│   ├── plugins/                 # Custom Airflow plugins
│   └── logs/                    # Task execution logs (auto-generated)
├── .env                         # Environment variables (git-ignored)
├── .env.example                 # Template for .env
├── docker-compose.yaml          # Service definitions
├── Makefile                     # Common operations
└── README.md
```

## Service URLs

| Service | URL | Default Credentials |
|---------|-----|-------------------|
| **Airflow UI** | http://localhost:8080 | `airflow` / `airflow` |
| **Flower (Celery)** | http://localhost:5555 | — |
| **PostgreSQL** | `localhost:5432` | user: `airflow` / `airflow` |

> **⚠️ Warning:** Change credentials in `.env` for any non-local environment.

## Adding DAGs

Place Python files in the `dags/` directory. They will be automatically picked up by the DAG processor.

## Configuration

- **Environment variables:** Edit `.env` (see `.env.example` for reference)
- **Airflow config:** Edit `config/airflow.cfg` — secrets are injected via env vars
- **Extra pip packages:** Set `_PIP_ADDITIONAL_REQUIREMENTS` in `.env`