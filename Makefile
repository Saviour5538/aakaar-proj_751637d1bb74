# Install dependencies for both backend and frontend
install:
	pip install -r requirements.txt
	cd frontend && npm install

# Start development servers for backend and frontend
dev:
	./scripts/dev.sh

# Build frontend for production
build:
	cd frontend && npm run build

# Run tests for backend and frontend
test:
	pytest
	cd frontend && npm test

# Start all services using Docker Compose
docker-up:
	docker-compose up --build -d

# Stop all services using Docker Compose
docker-down:
	docker-compose down

# Clean up Docker containers, images, and volumes
clean:
	docker-compose down -v
	docker system prune -f
	docker volume prune -f