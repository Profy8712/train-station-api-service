FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1


RUN mkdir -p /app/staticfiles /app/media && \
    groupadd -r appuser && \
    useradd -r -u 1000 -g appuser -d /app appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 775 /app/staticfiles /app/media


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY --chown=appuser:appuser requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


COPY --chown=appuser:appuser . .


USER appuser


CMD ["sh", "-c", "python manage.py migrate --noinput && \
     python manage.py collectstatic --noinput && \
     gunicorn train_station_api_service.wsgi:application --bind 0.0.0.0:8000"]
