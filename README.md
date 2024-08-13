# Weather Data API

This is a RESTful API built with FastAPI that serves weather data. It fetches data from OpenWeatherMap, stores it in a local database, and provides endpoints to create and retrieve weather information for specific cities and dates.

## Features

- Fetch weather data from OpenWeatherMap API
- Store weather data in a local SQLite database
- RESTful API with POST and GET endpoints
- Dockerized application for easy deployment

## Prerequisites

- Python 3.9+
- pip
- Docker and Docker Compose (for containerized deployment)

## Setup

1. Clone the repository:
git clone https://github.com/swathi0695/weather-data-api.git

cd weather-data-api

2. Create a `.env` file in the root directory and add your OpenWeatherMap API key:
OPENWEATHERMAP_API_KEY=your_api_key_here

### Using Docker

1. Build and run the Docker container:
docker-compose up --build
Copy
2. The API will be available at `http://localhost:8000`.
3. `http://localhost:8000/docs` - will give the API documentaion and also way to test out the apis

## API Endpoints

- `POST /weather`: Create weather data for a city on a specific date
- Request body: `{"city": "London", "date": "2023-05-20"}`

- `GET /weather`: Retrieve weather data for a city on a specific date
- Query parameters: `city` and `date`
- Example: `/weather?city=London&date=2023-05-20`

## Running Tests

To run the unit tests:
pytest
