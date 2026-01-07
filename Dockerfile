FROM python:3.11-slim

# Install uv (UV Manager)
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency files and install packages
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy the project files
COPY server .

# Expose the port
EXPOSE 8080

# Run the FastAPI app using UV Manager
CMD ["uv", "run", "server.app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]