# Reflectly - Time Reflection and Journaling

**Version:** 0.3.0 (Work in Progress)

> **Note:** This version is currently under active development and not yet finished. Some features may be incomplete or subject to change.

## Description
A time reflection and journaling web application designed to help you track work sessions, plan tasks, keep a productivity journal, and analyze progress through charts and statistics.

## Features

### Implemented (v0.3.0 - In Progress)
- **Modern Vue 3 Frontend** (NEW)
  - Single Page Application (SPA) architecture with Vue 3 and Vite
  - Vue Router for seamless navigation
  - Component-based UI architecture
  - Responsive landing page
  - Authentication pages (Login/Signup)
  - Dashboard layout with side navigation
  - User greeting component
  - Timer section component
  
- **JSON API for Authentication** (NEW)
  - RESTful API endpoints for signup, login, and logout
  - Separated from server-side rendering for better API/frontend separation
  
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
  - Modern dashboard UI (legacy templates in `frontend_backup/`)
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
- **Frontend:** Vue 3 + Vite + Vue Router (migrating from Jinja2 templates)
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
- Node.js >= 18.0.0 (for Vue 3 frontend)
- PostgreSQL
- Docker (optional)

## Installation

### Development Setup

#### Backend Setup
```bash
# Clone repository
git clone <repo-url>
cd Reflectly

# Install Python dependencies using uv
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and secrets

# Run database migrations
alembic upgrade head

# Start development server
uvicorn server.main:app --reload
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start Vue development server
npm run dev
```

The backend will run on `http://localhost:8000` and the frontend on `http://localhost:5173`

### Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## Deployment

For production deployment on VPS with Nginx and SSL:

**Quick deployment guide (Russian):** [deploy/README.ru.md](deploy/README.ru.md)  
**Detailed deployment guide (English):** [deploy/README.md](deploy/README.md)

```bash
# One-time setup: Get SSL certificate
./deploy/deploy.sh init

# Deploy/update application
./deploy/deploy.sh deploy
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
│   │   ├── api/               # API route handlers (v1)
│   │   └── middleware/        # Custom middleware
│   ├── core/                  # Core configuration and services
│   │   ├── config.py          # Application configuration
│   │   ├── jwt_config.py      # JWT configuration
│   │   └── logging_config.py  # Logging setup
│   ├── db/                    # Database models and repositories
│   │   ├── database.py        # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   └── repositories/      # Data access layer
│   ├── deps/                  # Dependencies and schemas
│   └── utils/                 # Utility functions
├── frontend/                  # Vue 3 SPA
│   ├── src/
│   │   ├── App.vue            # Root component
│   │   ├── main.js            # Vue application entry
│   │   ├── components/        # Vue components
│   │   │   ├── DashboardLayout.vue
│   │   │   ├── DashboardSideMenu.vue
│   │   │   ├── DashboardUserGreeting.vue
│   │   │   ├── LandingPage.vue
│   │   │   ├── LoginPage.vue
│   │   │   ├── SignupPage.vue
│   │   │   └── TimerSection.vue
│   │   └── assets/            # Static assets
│   ├── index.html
│   ├── vite.config.js         # Vite configuration
│   └── package.json
├── frontend_backup/           # Legacy server-side templates
│   ├── templates/             # Jinja2 templates (deprecated)
│   └── static/                # Legacy CSS/JS
├── alembic/                   # Database migrations
│   └── versions/
├── logs/                      # Application logs
├── pyproject.toml            # Python dependencies
├── docker-compose.yml        # Docker configuration
└── README.md
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
