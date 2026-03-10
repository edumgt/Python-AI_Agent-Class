.PHONY: run test docker-up docker-down

run:
	python -m uvicorn backend.app.main:app --reload --port 8080

test:
	python -m unittest discover -s backend/tests -p 'test_*.py'

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down
