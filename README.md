# Train Station API Service

## Overview
Dockerized Django REST Framework API for managing train station operations including routes,
journeys, tickets, and orders. Supports JWT authentication and provides comprehensive documentation through Swagger UI.

## Installation

Python 3.8+ and PostgreSQL required.

### Local Setup:
1. Clone the repository:
   bash
   git clone https://github.com/yourusername/train_station_api_service.git
   cd train_station_api_service
   
2.Create and activate virtual environment:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Install dependencies:

bash
pip install -r requirements.txt

4.Configure environment variables in .env:

DB_HOST=localhost
DB_NAME=train_station
DB_USER=youruser
DB_PASSWORD=yourpassword
SECRET_KEY=yoursecretkey

5.Apply migrations:

bash
python manage.py migrate

6.Run the server:

bash
python manage.py runserver

## Docker Setup:
Ensure Docker is installed, then run:
bash
docker-compose build
docker-compose up

## Access via Docker
fter running the API with Docker, follow these steps to access the service:

1. **Register a new user** (first-time setup):
   bash
   curl -X POST http://localhost:8000/api/user/register/ \
   -H "Content-Type: application/json" \
   -d '{
     "email": "your@email.com",
     "password": "yourpassword",
     "first_name": " ",
     "last_name": " "
   }'
2. Get JWT tokens (for authentication):
bash
curl -X POST http://localhost:8000/api/user/token/ \
-H "Content-Type: application/json" \
-d '{
  "email": "your@email.com",
  "password": "yourpassword"
}'
3. Use the access token in subsequent requests:

bash
curl http://localhost:8000/api/trains/ \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"

## Web Access:
API Browser: http://localhost:8000/

Admin Panel: http://localhost:8000/admin/

Swagger Docs: http://localhost:8000/api/doc/swagger/

## Docker-Specific Notes:
The database initializes automatically on first run
To reset everything:
bash
docker-compose down -v
docker-compose up

Check logs for errors:
bash
docker-compose logs -f

## Features
1.Custom User Model with JWT authentication 
2.Complete CRUD Operations for:
- Routes and Stations
- Trains and Train Types
- Journeys (Trips)
- Tickets and Orders 
3.Advanced Filtering for journeys by:
- Route
- Departure/Arrival times
- Train type

4.Pagination for all list endpoints

5.Modern REST API with Django REST Framework

6.Comprehensive Documentation via Swagger UI

7.Admin Dashboard for full system management

8.Database Relations as shown in schema:

## API Documentation
Interactive API documentation available at:
http://localhost:8000/api/doc/

