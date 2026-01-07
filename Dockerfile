FROM python:3.11-slim

# Install uv CLI and uvicorn ASGI server so `uv sync` and `uv run` work
RUN pip install --no-cache-dir "uv" "uvicorn[standard]"
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies and install via uv's lockfile (use python -m uv to avoid missing script entrypoint)
COPY pyproject.toml uv.lock ./
RUN uv sync

# Copy project files (server, frontend и т.д.)
COPY . .

# Expose port
EXPOSE 8080

# Run FastAPI app using uv run (via python -m to avoid PATH issues)
# Pass -m to tell uv to run a Python module target of the form module:callable
CMD ["uv", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--cport", "8080" ,"--reload"]