FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1
ENV DOCKER_ENV 1

# Create application directories
RUN mkdir -p /app/staticfiles /app/media
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Set permissions
RUN chown -R 1000:1000 /app && \
    chmod -R 755 /app/staticfiles /app/media

# Create and switch to non-root user
RUN useradd -u 1000 -s /bin/bash -d /app appuser
USER appuser

# Runtime command
CMD ["sh", "-c", "python manage.py migrate --noinput && \
     python manage.py collectstatic --noinput && \
     gunicorn train_station_api_service.wsgi:application --bind 0.0.0.0:8000"]
