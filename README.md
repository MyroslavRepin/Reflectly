# Reflectly - Code Time Tracker

Track your coding sessions, reflect on productivity, and build better habits.

**Version:** 0.6.0  
**Repository:** https://github.com/MyroslavRepin/Reflectly.git

> This project is actively under development. Some features may be incomplete or subject to change.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Quick Start

Get up and running in 5 minutes!

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/MyroslavRepin/Reflectly.git
cd Reflectly

# Start the application
docker-compose up -d

# Access the app
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/MyroslavRepin/Reflectly.git
cd Reflectly

# Backend setup (in main directory)
uv sync
cp .env.example .env
alembic upgrade head
uvicorn server.main:app --reload

# Frontend setup (in new terminal)
cd frontend
npm install
npm run dev

# Access the app
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

---

## Features

### Currently Available

- **Time Tracking** ⏱️
  - Start/stop timer for coding sessions
  - Real-time elapsed time display
  - Session history and statistics

- **Authentication** 🔐
  - User registration and login
  - Secure JWT-based sessions
  - Persistent login with refresh tokens

- **Dashboard & Settings** 📊
  - Redesigned dashboard with intuitive navigation
  - Detailed session history with title and description editing
  - **Enhanced entry modal with preview and edit modes**
  - **Individual time entry viewing and editing**
  - User profile management and settings module
  - Secure account deletion (soft delete)

- **Modern UI** 🎨
  - Responsive Vue 3 single-page application
  - Works on desktop and mobile
  - Dark-themed design

### Coming Soon

- Productivity journal

---

## Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next-generation build tool
- **Vue Router** - Client-side routing
- **Axios** - HTTP client

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - Python ORM (async)
- **Alembic** - Database migrations
- **AuthX** - Authentication & authorization

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server (production)

### Other
- **Loguru** - Logging
- **Argon2** - Password hashing
- **JWT** - Secure tokens

---

## Prerequisites

### Minimum Requirements

- **Python** >= 3.11
- **Node.js** >= 18.0.0
- **PostgreSQL** >= 12

### Using Docker (No local setup needed)

- **Docker** >= 20.10
- **Docker Compose** >= 2.0

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/MyroslavRepin/Reflectly.git
cd Reflectly
```

### Step 2: Backend Setup

#### Option A: Using `uv` (Recommended)

```bash
# Install Python dependencies
uv sync

# Copy environment file
cp .env.example .env

# Edit .env with your configuration (database credentials, JWT secret, etc.)
# nano .env  # or use your preferred editor

# Run database migrations
alembic upgrade head
```

#### Option B: Using `pip` and `venv`

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env

# Run database migrations
alembic upgrade head
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Return to project root (optional, for running from main dir)
cd ..
```

### Step 4: Database Setup

```bash
# Ensure PostgreSQL is running, then create database and run migrations
alembic upgrade head
```

---

## Running the Application

### Option 1: Local Development (Two Terminal Windows)

**Terminal 1 - Backend:**
```bash
# From project root
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
# From project root
cd frontend
npm run dev
```

**Access the application:**
- Frontend: http://localhost:5173
- API Swagger Docs: http://localhost:8000/docs
- API ReDoc: http://localhost:8000/redoc

### Option 2: Docker Compose (Single Command)

```bash
# From project root
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

**Access the application:**
- Frontend: http://localhost:5173
- API Swagger Docs: http://localhost:8000/docs

---

## Configuration

### Environment Variables

Key variables in `.env` file (see `.env.example` for all options):

```dotenv
# Database
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=reflectly
DB_URL_FULL=postgresql+asyncpg://user:password@host:port/database

# JWT Authentication
JWT_SECRET_KEY=your_secret_key_here
JWT_ACCESS_TOKEN_EXPIRES_SECONDS=30
JWT_ALGORITHM=HS256

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
SERVER_DEBUG=True

# Frontend Environment
VITE_FRONTEND_ENV=dev  # 'dev' or 'prod'
```

### API URL Configuration

The frontend automatically switches between dev and prod API URLs based on `VITE_FRONTEND_ENV`:

- **Development:** `http://localhost:8080/api/v1`
- **Production:** `https://reflectly.myroslavrepin.com/api/v1`

See [API_CONFIGURATION.md](API_CONFIGURATION.md) for detailed setup.

---

## Project Structure

```
Reflectly/
├── frontend/                          # Vue 3 Frontend Application
│   ├── src/
│   │   ├── config/
│   │   │   └── api.js                # Environment-based API configuration
│   │   ├── components/               # Vue components
│   │   │   ├── DashboardLayout.vue   # Main dashboard layout
│   │   │   ├── DashboardEntries.vue  # Session history
│   │   │   ├── DashboardTimerSection.vue  # Timer interface
│   │   │   ├── Notification.vue      # Reusable notifications
│   │   │   ├── Settings/             # Settings module
│   │   │   ├── LoginPage.vue         # Authentication
│   │   │   └── SignupPage.vue        # Registration
│   │   ├── assets/                   # Styles and static files
│   │   ├── App.vue                   # Root component
│   │   └── main.js                   # Entry point
│   ├── index.html
│   ├── vite.config.js                # Build configuration
│   └── package.json                  # NPM dependencies
│
├── server/                            # FastAPI Backend
│   ├── main.py                        # Application entry point
│   ├── app/
│   │   ├── api/                      # API endpoints
│   │   │   ├── auth.py               # Authentication routes
│   │   │   ├── dashboard.py          # Dashboard routes
│   │   │   └── v1/                   # API v1
│   │   └── middleware/               # Custom middleware
│   ├── core/                         # Configuration
│   │   ├── config.py                 # App settings
│   │   ├── jwt_config.py             # JWT setup
│   │   └── logging_config.py         # Logging setup
│   ├── db/                           # Database
│   │   ├── models/                   # SQLAlchemy models
│   │   ├── repositories/             # Data access layer
│   │   └── database.py               # Connection setup
│   ├── deps/                         # Dependencies & schemas
│   └── utils/                        # Helper functions
│
├── alembic/                          # Database Migrations
│   └── versions/                     # Migration scripts
│
├── deploy/                           # Deployment scripts
│   ├── nginx/                        # Nginx configuration
│   └── README.md                     # Deployment guide
│
├── docker-compose.yml                # Docker setup
├── Dockerfile                        # Container definition
├── pyproject.toml                    # Python dependencies
├── uv.lock                           # Dependency lock file
├── .env.example                      # Environment template
├── alembic.ini                       # Migration config
└── README.md                         # This file
```

---

## API Documentation

### Interactive Docs

Once the backend is running, access interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Main Endpoints

**Authentication:**
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token

**Timer & Entries:**
- `GET /api/v1/time-entries` - Get all sessions
- `GET /api/v1/time-entries/current-running` - Get active session
- `GET /api/v1/time-entries/{entry_id}` - Get specific time entry
- `POST /api/v1/time-entries/start` - Start new session
- `POST /api/v1/time-entries/pause` - Pause current session
- `PATCH /api/v1/time-entries/stop` - Stop current session
- `PATCH /api/v1/time-entries/{entry_id}` - Update session details
- `DELETE /api/v1/time-entries/{entry_id}` - Delete session

**User Profile:**
- `GET /api/v1/users/me` - Get current user profile
- `PATCH /api/v1/users/me` - Update user profile
- `DELETE /api/v1/users/me` - Soft delete account

---

## Deployment

### Local Production Build

```bash
# Build frontend
cd frontend
npm run build
# Output: frontend/dist/

# Run backend with production settings
VITE_FRONTEND_ENV=prod uvicorn server.main:app --host 0.0.0.0 --port 8000
```

### VPS Deployment (with Nginx & SSL)

See detailed guides:
- **English:** [deploy/README.md](deploy/README.md)
- **Russian:** [deploy/README.ru.md](deploy/README.ru.md)

Quick deployment:
```bash
# One-time: Setup SSL certificates
./deploy/deploy.sh init

# Deploy or update
./deploy/deploy.sh deploy
```

---

## Contributing

We welcome contributions! Here's how to help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python
- Use type hints throughout
- Write meaningful comments explaining "why", not "what"
- No print statements - use logging instead
- Include tests for new features

---

## Troubleshooting

### Issue: "Cannot connect to database"
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify connection string format

### Issue: "Port 8000 already in use"
- Change port: `uvicorn server.main:app --port 8001`
- Or kill existing process: `lsof -ti:8000 | xargs kill -9`

### Issue: "Frontend can't reach backend API"
- Check `VITE_FRONTEND_ENV` in `.env`
- Verify backend is running on correct port
- Check browser console for CORS errors

### Issue: "npm install fails"
- Clear cache: `npm cache clean --force`
- Delete `node_modules`: `rm -rf node_modules`
- Try again: `npm install`

Need more help? Check [API_CONFIGURATION.md](API_CONFIGURATION.md) for frontend API setup.

---

## License

MIT License - see LICENSE file for details

---

## Support

- Create an issue on [GitHub](https://github.com/MyroslavRepin/Reflectly/issues)
- Check existing documentation in `deploy/` and `docs/` folders

---

**Happy tracking! Track your time, reflect on progress, build better habits.**
