# Chat_Project

A Django-based real-time chat application with WebSocket support, user authentication, and notifications. Dockerized for easy local development.

## Features
- Real-time chat using Django Channels
- JWT authentication
- WebSocket notifications
- PostgreSQL and Redis integration
- Docker Compose setup for local development

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.10+

### Local Development
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd Chat_Project
   ```
2. Copy `.env` template and configure your secrets:
   ```sh
   cp core/.env.example core/.env
   # Edit core/.env as needed
   ```
3. Build and start the containers:
   ```sh
   make build-local
   ```
4. To start the containers:
    ```sh
    make run-local
    ```
5. Access the app at [http://localhost:8001](http://localhost:8001)

### Running Migrations
```sh
make migrate
```

### Running Tests
```sh
docker-compose -f local.yml exec web python manage.py test
```

## Project Structure
- `core/` - Django settings and configuration
- `chatapp/` - Chat logic and WebSocket consumers
- `accounts/` - User authentication and management
- `common/` - Shared utilities and functions

## License
MIT
