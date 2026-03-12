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
| **postgres** | Metadata database |
| **redis** | Celery message broker |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) ≥ 24.0
- [Docker Compose](https://docs.docker.com/compose/install/) ≥ 2.20
- At least **4 GB RAM** allocated to Docker

## Quick Start

```bash
# 1. Copy the example env file and edit as needed
cp .env.example .env

# 2. Start all services
docker compose up -d

# 3. Wait for the init container to finish (~60 s on first run)
docker compose logs -f airflow-init

# 4. Open the Airflow UI
open http://localhost:8080
```

## Default Credentials

| Service | Username | Password |
|---------|----------|----------|
| Airflow UI | `airflow` | `airflow` |
| Postgres | `airflow` | `airflow` |

> **⚠️ Warning:** Change these in `.env` for any non-local environment.

## Project Structure

```
.
├── config/
│   └── airflow.cfg          # Airflow configuration
├── dags/                    # Place your DAG files here
│   └── hello_world.py       # Example DAG
├── logs/                    # Task execution logs (auto-generated)
├── plugins/                 # Custom Airflow plugins
├── .env                     # Environment variables (gitignored)
├── .env.example             # Template for .env
├── docker-compose.yaml      # Service definitions
├── Makefile                 # Common operations
└── README.md
```

## Common Operations

```bash
make up          # Start services in background
make down        # Stop services
make restart     # Restart all services
make logs        # Follow all service logs
make reset       # Stop services, remove volumes, and restart fresh
make status      # Show running containers
make shell       # Open a bash shell in the API server
```

## Adding DAGs

Place Python files in the `dags/` directory. They will be automatically picked up by the DAG processor.

## Configuration

- **Environment variables:** Edit `.env` (see `.env.example` for reference)
- **Airflow config:** Edit `config/airflow.cfg` — secrets are injected via env vars
- **Extra pip packages:** Set `_PIP_ADDITIONAL_REQUIREMENTS` in `.env`