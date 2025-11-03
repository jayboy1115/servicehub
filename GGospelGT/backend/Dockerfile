# Backend Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configure pip for more resilient installs
ENV PIP_DEFAULT_TIMEOUT=120 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with upgraded pip and extended timeout
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=120 -r requirements.txt

# Copy source code into /app so 'backend' is on sys.path
COPY . .

# Expose port
EXPOSE 8001

# Start the application via uvicorn using package path
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8001"]