# Deployment Guide

## Quick Start

### Prerequisites
- VPS with Docker and Docker Compose installed
- Node.js >= 18.0.0 (for building Vue frontend)
- Domain pointing to your VPS IP address
- Ports 80 and 443 open in firewall

### Step 1: Clone and Configure

```bash
git clone <your-repo> && cd Reflectly
cp .env.example .env
nano .env
```

Update `.env` with your values:
```env
DOMAIN=yourdomain.com
EMAIL=your@email.com
POSTGRES_PASSWORD=strong_password
DATABASE_URL=postgresql+asyncpg://reflectly_user:strong_password@db:5432/reflectly
```

### Step 2: Initial Setup (SSL Certificate)

```bash
chmod +x deploy/deploy.sh
./deploy/deploy.sh init
```

This will:
- Start Nginx
- Obtain SSL certificate from Let's Encrypt
- Configure Nginx with your domain

### Step 3: Deploy Application

```bash
./deploy/deploy.sh deploy
```

This will:
- Pull latest code from Git
- Build and start all services
- Run database migrations

Your application will be available at `https://yourdomain.com`

## Commands

```bash
# Deploy/update application
./deploy/deploy.sh deploy

# View logs
./deploy/deploy.sh logs
./deploy/deploy.sh logs nginx

# Restart services
./deploy/deploy.sh restart
./deploy/deploy.sh restart nginx

# Stop all services
./deploy/deploy.sh stop
```

## Manual Commands

```bash
# Check status
docker compose ps

# View logs
docker compose logs -f server

# Run migrations
docker compose exec server uv run alembic upgrade head

# Database backup
docker compose exec db pg_dump -U reflectly_user reflectly > backup.sql

# Access database
docker compose exec db psql -U reflectly_user reflectly
```

## Troubleshooting

**SSL certificate fails:**
```bash
# Check domain DNS
dig yourdomain.com +short

# Check Nginx logs
docker compose logs nginx
```

**502 Bad Gateway:**
```bash
# Check if server is running
docker compose ps server
docker compose logs server
```

**Database connection error:**
```bash
docker compose exec db psql -U reflectly_user reflectly
```

## Security

- Never commit `.env` file
- Use strong passwords
- Keep Docker images updated
- Setup regular database backups
- Monitor logs for suspicious activity

## Project Structure

```
Reflectly/
├── deploy/
│   ├── nginx/
│   │   └── conf.d/
│   │       └── reflectly.conf
│   ├── certbot/
│   │   ├── conf/          # SSL certificates
│   │   └── www/           # ACME challenge
│   ├── deploy.sh          # Deployment script
│   └── README.md          # This file
├── docker-compose.yml
├── .env                   # Your configuration (DO NOT COMMIT)
└── .env.example           # Example configuration
```
