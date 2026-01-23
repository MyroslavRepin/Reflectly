# Deployment Guide

## Cloudflare Tunnel Setup

### Prerequisites
- Docker and Docker Compose installed on the server
- Cloudflare account with a configured tunnel

### Setup Steps

1. **Copy configuration files to the server**

```bash
# Create the cloudflared directory
sudo mkdir -p /etc/cloudflared

# Copy the tunnel credentials file
sudo cp deploy/cloudflared/b6527f78-2aa5-46fc-9e73-786f44810f2d.json /etc/cloudflared/

# Copy the tunnel configuration
sudo cp deploy/cloudflared/config.yml /etc/cloudflared/

# Set proper permissions
sudo chmod 600 /etc/cloudflared/b6527f78-2aa5-46fc-9e73-786f44810f2d.json
sudo chmod 644 /etc/cloudflared/config.yml
```

2. **Verify files are in place**

```bash
ls -la /etc/cloudflared/
```

You should see:
- `b6527f78-2aa5-46fc-9e73-786f44810f2d.json` (credentials file)
- `config.yml` (tunnel configuration)

3. **Start the services**

```bash
# Start all services (server + cloudflared)
docker-compose up -d

# Check if services are running
docker-compose ps

# View cloudflared logs
docker-compose logs -f cloudflared
```

4. **Verify tunnel is working**

Check the Cloudflare dashboard to confirm the tunnel is connected, or test by accessing your domain.

### Troubleshooting

**If you see "Cannot determine default origin certificate path" error:**
- Ensure files are copied to `/etc/cloudflared/` on the server
- Check file permissions (credentials file should be `600`)

**If cloudflared can't connect to the server:**
- Verify the server container is running: `docker-compose ps`
- Check docker-compose.yml has the correct service names
- Ensure cloudflared depends_on server in docker-compose.yml

### Updating Configuration

After modifying `deploy/cloudflared/config.yml`:

```bash
# Copy updated config
sudo cp deploy/cloudflared/config.yml /etc/cloudflared/

# Restart cloudflared
docker-compose restart cloudflared
```

## Server Deployment

### Build and Deploy

```bash
# Build the application
docker-compose build server

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f server
```

### Database Migrations

```bash
# Run migrations
docker-compose exec server alembic upgrade head

# Create new migration
docker-compose exec server alembic revision --autogenerate -m "description"
```
