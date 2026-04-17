# Airflow 3 + CeleryExecutor + MinIO Remote Logging

Apache Airflow 3 running on Docker Compose with the **CeleryExecutor** backend and **MinIO** for remote log storage (S3-compatible).

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
| **minio** | S3-compatible object storage for remote logs (port `9000/9001`) |
| **minio-init** | Initializes MinIO buckets on startup |

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
│   │   └── airflow.cfg          # Airflow configuration (with S3 remote logging)
│   ├── dags/                    # Place your DAG files here
│   │   └── hello_world.py       # Example DAG
│   ├── plugins/                 # Custom Airflow plugins
│   └── logs/                    # Local task execution logs (backed up to MinIO)
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
| **MinIO API** | http://localhost:9000 | `minioadmin` / `minioadmin` |
| **MinIO Console** | http://localhost:9001 | `minioadmin` / `minioadmin` |
| **PostgreSQL** | `localhost:5432` | user: `airflow` / `airflow` |

> **⚠️ Warning:** Change credentials in `.env` for any non-local environment.

## MinIO & Remote Logging

This setup uses **MinIO** (S3-compatible storage) to store Airflow task logs remotely. Key features:

### Configuration
- Task logs are automatically uploaded to MinIO's `airflow-logs` bucket
- The `minio_conn` connection is automatically created via the `AIRFLOW_CONN_MINIO_CONN` environment variable
- Remote logging is enabled in `airflow.cfg` with the `S3TaskHandler`

### MinIO Console
Access MinIO's web console at **http://localhost:9001** to:
- Browse the `airflow-logs` bucket and task logs
- Manage credentials and buckets
- Monitor MinIO health and usage

### Accessing Logs

**From Airflow UI:**
- All task logs in the Airflow UI will show remote logs from MinIO
- Local logs are kept until `delete_local_logs` policy is applied

**Directly from MinIO:**
```bash
# Using MinIO client (mc)
docker exec minio-init mc ls myminio/airflow-logs/
```

### Configuration Details
Edit `airflow/config/airflow.cfg` [logging] section to customize:
```ini
remote_logging = True                     # Enable remote logging
remote_log_conn_id = minio_conn          # Connection ID
remote_base_log_folder = s3://airflow-logs  # S3 bucket path
logging_config_class = airflow.providers.amazon.aws.log_handler.S3TaskHandler
```

## Adding DAGs

Place Python files in the `dags/` directory. They will be automatically picked up by the DAG processor.

## Configuration

- **Environment variables:** Edit `.env` (see `.env.example` for reference)
- **Airflow config:** Edit `config/airflow.cfg` — secrets are injected via env vars
- **Extra pip packages:** Set `_PIP_ADDITIONAL_REQUIREMENTS` in `.env` (already includes `apache-airflow-providers-amazon`)