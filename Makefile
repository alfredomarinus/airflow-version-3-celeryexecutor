.PHONY: up down restart logs reset status shell

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

reset:
	docker compose down -v
	docker compose up -d

status:
	docker compose ps

shell:
	docker compose exec airflow-api-server bash