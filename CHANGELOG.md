# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - Unreleased (Work in Progress)

**Note:** This version is currently under development and not yet finished.

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

### In Progress
- Completing Vue component integration
- Connecting Vue frontend with FastAPI backend
- Migrating remaining features from legacy templates
- Testing and debugging new architecture

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

