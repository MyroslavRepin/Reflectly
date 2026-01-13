# Reflectly - Time Reflection and Journaling

**Version:** 0.2.0

## Description
A time reflection and journaling web application designed to help you track work sessions, plan tasks, keep a productivity journal, and analyze progress through charts and statistics.

## Features

### Implemented (v0.2.0)
- **Time Tracking**
  - Start/stop timer functionality
  - Time entries database model
  - API endpoints for timer control (`/api/v1/timer/start`, `/api/v1/timer/stop`, `/api/v1/timer/current`)
  - Track coding sessions with timestamps
  - User-specific time entry tracking
  
- **User Authentication**
  - Secure signup and login system
  - JWT-based authentication with access and refresh tokens
  - Password hashing with Argon2
  - HttpOnly cookies for secure token storage
  - Automatic token refresh middleware
  - Token refresh endpoint (`/auth/refresh`)
  
- **Dashboard**
  - Modern dashboard UI templates
  - Session time tracking interface
  - Project overview sections
  - Responsive design for mobile and desktop
  
- **User Management**
  - User registration with email and username
  - Password validation
  - User profile management
  - Database-backed user storage

- **Infrastructure**
  - PostgreSQL database with async support (asyncpg)
  - Alembic migrations for database schema management
  - Docker containerization support
  - Comprehensive logging with Loguru
  - Environment-based configuration
  - Time entries table with foreign key relationships

### Planned
- Productivity journal
- Charts and statistics for time and tasks
- Task planning and prioritization
- Project management and categorization
- Optional AI journal analysis

## Tech Stack
- **Backend:** FastAPI + PostgreSQL + SQLAlchemy (async)
- **Frontend:** Jinja2 Templates (Vue.js planned)
- **Authentication:** JWT tokens with AuthX
- **Database:** PostgreSQL with asyncpg driver
- **Migrations:** Alembic
- **Logging:** Loguru
- **Password Hashing:** Argon2
- **Containerization:** Docker + Docker Compose
- **Charts / Visualization:** Chart.js / Plotly (planned)
- **Optional AI Module:** OpenAI API (planned)

## Prerequisites
- Python >= 3.14
- PostgreSQL
- Docker (optional)

## Installation

### Development Setup
```bash
# Clone repository
git clone <repo-url>
cd Reflectly

# Install dependencies using uv
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and secrets

# Run database migrations
alembic upgrade head

# Start development server
uvicorn server.main:app --reload
```

### Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## Configuration
Key environment variables (see `.env.example`):
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret key for JWT token generation
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiration time
- `JWT_REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiration time
- `SERVER_HOST` - Server host address
- `SERVER_PORT` - Server port

## Project Structure
```
Reflectly/
├── server/
│   ├── main.py                 # FastAPI application entry point
│   ├── app/
│   │   ├── api/               # API route handlers
│   │   └── middleware/        # Custom middleware
│   ├── core/                  # Core configuration and services
│   ├── db/                    # Database models and repositories
│   ├── deps/                  # Dependencies and schemas
│   └── utils/                 # Utility functions
├── frontend/
│   ├── static/                # CSS, JS files
│   └── templates/             # Jinja2 templates
├── alembic/                   # Database migrations
├── logs/                      # Application logs
├── pyproject.toml            # Project dependencies
└── docker-compose.yml        # Docker configuration
```

## API Documentation
Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing
```bash
# Run tests (when implemented)
pytest
```

## Contributing
Contributions are welcome! Please ensure:
- Code follows PEP 8 standards
- Type hints are used throughout
- Proper logging (no print statements)
- Tests are included for new features

## License
MIT
