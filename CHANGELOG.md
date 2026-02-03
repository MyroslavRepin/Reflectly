# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-02-02

### Added
- **Environment-Based API Configuration**
  - Single `.env` file controls frontend environment (dev/prod)
  - `VITE_FRONTEND_ENV` variable to switch between development and production
  - Config file `frontend/src/config/api.js` for centralized API URL management
  - Development API URL: `http://localhost:8080/api/v1`
  - Production API URL: `https://reflectly.myroslavrepin.com/api/v1`
  - Console logging showing active environment on app load

- **Build & Configuration**
  - Vite alias configuration for clean `@/` imports
  - Dockerfile updated to copy `.env` during build
  - Enhanced `vite.config.js` with proper module resolution

- **Documentation**
  - Completely rewritten `README.md` with user-friendly structure
  - Quick Start section with Docker and manual setup options
  - Step-by-step installation guide
  - Clear API configuration documentation (`API_CONFIGURATION.md`)
  - Troubleshooting section
  - Project structure overview
  - Deployment instructions

### Changed
- **All API Calls in Components Updated**
  - Updated `LoginPage.vue` to use `API_BASE_URL` from config
  - Updated `SignupPage.vue` to use `API_BASE_URL` from config
  - Updated `DashboardEntries.vue` to use `API_BASE_URL` from config
  - Updated `DashboardTimerSection.vue` to use `API_BASE_URL` from config
  - Removed hardcoded API URLs from all components
  - Components now import `API_BASE_URL` from `@/config/api`

- **Frontend Configuration**
  - `vite.config.js` now includes resolve alias for `@/` path imports
  - Environment variables read from project root `.env` file
  - Build process now respects `VITE_FRONTEND_ENV` setting

### Removed
- Centralized API service layer (components manage their own axios instances)
- Hardcoded API URLs from all components

### Fixed
- Frontend environment variables not being read by Vite during Docker build
- Inconsistent API URLs across components
- Frontend caching issues by ensuring proper build invalidation

### Infrastructure
- Docker build process improved to include `.env` file
- Environment-based frontend builds in Docker
- Production-ready deployment configuration

### Docs
- New `API_CONFIGURATION.md` with detailed setup guide
- Restructured `README.md` for better user experience
- Quick start options (Docker and manual)
- Clear configuration sections

## [0.3.0] - 2026-01-15

### Added
- **Vue 3 Frontend**
  - Initial Vue 3 setup with Vite build system
  - Vue Router for client-side routing
  - Authentication pages (Login, Signup)
  - Landing page component
  - Dashboard layout component with side menu
  - User greeting component for dashboard
  - Timer section component for time tracking
  
- **Authentication API (JSON)**
  - JSON-based signup endpoint
  - JSON-based login endpoint
  - Logout endpoint
  - API endpoints separated from server-side rendered routes

### Changed
- **Frontend Architecture Refactor**
  - Migrated from server-side rendering (Jinja2) to Vue 3 SPA
  - Moved legacy server-side HTML/CSS templates to `frontend_backup/`
  - Restructured Vue.js project with component-based architecture
  - Enhanced landing page design with modern UI
  - Improved dashboard layout structure
  
- **Project Organization**
  - Separated frontend concerns: Vue components vs legacy templates
  - Better file organization for maintainability
  - Version bumped to 0.3.0


## [0.2.0] - 2026-01-12

### Added
- **Time Tracking System**
  - Time entries database model with user foreign key relationships
  - TimeEntriesRepository for database operations
  - API endpoint `/api/v1/timer/start` to start tracking time
  - API endpoint `/api/v1/timer/stop` to stop active timer
  - API endpoint `/api/v1/timer/current` to get current running timer
  - Entry creation schema (EntryCreate)
  - Database migration for time_entries table
  
- **Token Management**
  - Token refresh endpoint `/auth/refresh` for renewing access tokens
  - Refresh token router in API v1
  
- **Dashboard UI**
  - Modern dashboard template with session tracking interface
  - Dashboard v2 template with improved design
  - Project overview cards
  - Session timer display
  - Settings modal functionality
  - Responsive design for mobile and desktop
  - Navigation menu with dashboard, projects, and settings sections
  
- **API Organization**
  - API v1 directory structure for versioned endpoints
  - Proper separation of concerns with routers
  
### Changed
- Updated project version from 0.1.1 to 0.2.0
- Enhanced dashboard route to support time tracking features
- Improved error handling in timer endpoints with proper HTTP status codes
- Added conflict detection for running timers (409 status)

### Fixed
- Timer validation to prevent multiple simultaneous timers per user
- Proper error logging without exposing internal errors to users
- Database transaction rollback on time entry creation errors

### Infrastructure
- Added time_entries table migration (0cc9e1ff9c19)
- Removed unused columns migration (e465ecbe595f)
- Enhanced logging with user context in time tracking operations

## [0.1.1] - 2026-01-10

### Added
- User authentication system with JWT tokens
- Login and signup functionality
- Password validation for signup forms
- User schema for account creation
- Database models for user management
- Alembic migrations for database schema management
- Users table in database
- Logging configuration using Loguru
- Configuration files for FastAPI project
- Initial project structure with frontend templates
- Docker support with Dockerfile
- Environment configuration with .env.example

### Changed
- Updated project version from 0.1.0 to 0.1.1
- Updated project description to "A time reflection and journaling web application"
- Improved refresh token handling
- Enhanced server configuration and token management
- Updated .env.example with placeholder values

### Fixed
- Token decoding return format in jwt_service
- Typos in Dockerfile
- Authentication bugs in user login flow

### Infrastructure
- Added Alembic for database migrations
- PostgreSQL database setup with asyncpg
- Initial FastAPI application configuration
- Docker Compose setup for containerized deployment

## [0.1.0] - Initial Release

### Added
- Initial project setup
- Basic FastAPI application
- README documentation
- Project structure planning

