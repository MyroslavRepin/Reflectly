# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

