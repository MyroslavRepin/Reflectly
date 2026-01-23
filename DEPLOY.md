# Deployment Guide

## Cloudflare Tunnel Setup

### Prerequisites
- Cloudflare account with an active zone for `reflectly.myroslavrepin.com`
- Access to the Cloudflare Zero Trust dashboard (Tunnels > Named Tunnels)
- Docker + Docker Compose installed on the target host
- Local machine with a browser to complete `cloudflared tunnel login`

### Required Files (stored in `deploy/cloudflared/`)
- `config.yml`: Provided in this repo; maps the hostname to `reflectly-server:8080`
- `b6527f78-2aa5-46fc-9e73-786f44810f2d.json`: Tunnel credential downloaded from Cloudflare
- `cert.pem`: Origin certificate produced by `cloudflared tunnel login` **(not committed; ignored via `.gitignore`)**

> Keep `cert.pem` and the credential JSON outside of version control in prod. The
> copies under `deploy/cloudflared/` should come from your secret store or be
> synced securely (scp/rsync) before deploying.

### 1. Authenticate and Download the Origin Certificate
Run these commands **on a workstation with a browser**:

```bash
brew install cloudflared              # or use apt/yum/choco
cloudflared tunnel login              # pop up browser, pick the zone
ls ~/.cloudflared                     # cert.pem now exists here
cp ~/.cloudflared/cert.pem /path/to/Reflectly/deploy/cloudflared/cert.pem
chmod 600 /path/to/Reflectly/deploy/cloudflared/cert.pem
```

### 2. Create (or Reuse) the Tunnel and Credentials
If the tunnel does not yet exist:

```bash
cloudflared tunnel create reflectly-tunnel
cloudflared tunnel route dns reflectly-tunnel reflectly.myroslavrepin.com
```

Copy the generated credential file into the repo (or secret storage) and lock it
down:

```bash
cp ~/.cloudflared/*.json /path/to/Reflectly/deploy/cloudflared/
chmod 600 /path/to/Reflectly/deploy/cloudflared/*.json
```

### 3. Review the Docker Compose Integration
`docker-compose.yml` mounts the Cloudflare assets directly:

```yaml
cloudflared:
  image: cloudflare/cloudflared:latest
  command: tunnel run reflectly-tunnel
  volumes:
    - ./deploy/cloudflared:/etc/cloudflared:ro
  environment:
    - TUNNEL_ORIGIN_CERT=/etc/cloudflared/cert.pem
```

`config.yml` already specifies:

```yaml
credentials-file: /etc/cloudflared/b6527f78-2aa5-46fc-9e73-786f44810f2d.json
origincert: /etc/cloudflared/cert.pem
```

This resolves the "Cannot determine default origin certificate path" error,
provided that `cert.pem` exists inside `deploy/cloudflared/` before you start
Docker.

### 4. Start the Stack
From the project root:

```bash
docker compose pull cloudflared
docker compose up -d server cloudflared
```

Useful follow-ups:

```bash
docker compose ps
docker compose logs -f cloudflared
```

### 5. Verify the Tunnel End-to-End
1. **Container logs** – look for `Connection established` and `Connected to
   Cloudflare` lines:
   ```bash
   docker compose logs cloudflared | grep -E "Connected|Established"
   ```
2. **Cloudflare dashboard** – the tunnel should show as `Healthy` in Zero Trust.
3. **HTTP check via Cloudflare**:
   ```bash
   curl -I https://reflectly.myroslavrepin.com
   ```
   Expect a `200`/`302` served by the FastAPI app (proxied through Cloudflare).
4. **Inspect tunnel status** (optional, requires local cloudflared auth):
   ```bash
   cloudflared tunnel info reflectly-tunnel
   ```

### Troubleshooting

| Symptom | Likely Cause | Resolution |
| --- | --- | --- |
| `Cannot determine default origin certificate path` | `cert.pem` missing from the mounted folder | Run `cloudflared tunnel login`, copy `cert.pem` into `deploy/cloudflared/`, ensure permissions `600`, redeploy |
| `Failed to load tunnel credentials` | JSON file name mismatches config | Update `config.yml` `credentials-file` path or copy the correct JSON from Cloudflare |
| Tunnel shows `Degraded` or `Inactive` | Docker service cannot reach FastAPI origin | Confirm `reflectly-server` container is running and listening on `8080`; inspect `docker compose logs server` |
| Browser shows 502/522 | DNS hostname not routed to the tunnel | Re-run `cloudflared tunnel route dns reflectly-tunnel reflectly.myroslavrepin.com` and wait for DNS propagation |
| Permission denied reading cert | Host copied files with restrictive ownership | `chown root:root deploy/cloudflared/* && chmod 600 *.json *.pem` before `docker compose up` |

## Server Deployment

### Build and Deploy

```bash
docker compose build server
docker compose up -d
docker compose logs -f server
```

### Database Migrations

```bash
docker compose exec server alembic upgrade head
docker compose exec server alembic revision --autogenerate -m "description"
```

Re-run the verification steps in the previous section whenever you roll out a
new server build to ensure the Cloudflare tunnel still reaches the updated app.
