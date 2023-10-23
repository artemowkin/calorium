dev:
	docker compose -f docker-compose.dev.yml up --build
	docker compose -f docker-compose.dev.yml down
prod:
	docker compose -f docker-compose.prod.yml up --build
