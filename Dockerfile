FROM python:3.11-slim

# Install Node.js 20.x
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv CLI and uvicorn ASGI server so `uv sync` and `uv run` work
RUN pip install --no-cache-dir "uv" "uvicorn[standard]"
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies and install via uv's lockfile (use python -m uv to avoid missing script entrypoint)
COPY pyproject.toml uv.lock ./
RUN uv sync

# Copy frontend source and build
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm ci

COPY frontend/ ./frontend/

# Clean any existing dist directory and build fresh
RUN rm -rf ./frontend/dist && cd frontend && npm run build

# Verify dist was created
RUN test -d ./frontend/dist || (echo "ERROR: Frontend build failed, dist directory not created" && exit 1)

# Copy server files
COPY server/ ./server/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Expose port
EXPOSE 8000

# Run FastAPI app using uv run (via python -m to avoid PATH issues)
# Pass -m to tell uv to run a Python module target of the form module:callable
CMD ["uv", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]