import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
import requests
from .database import get_db
from .crud import get_weather_data, create_weather_data
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class WeatherRequest(BaseModel):
    city: str
    date: date

@app.post("/weather")
def post_weather_data(weather_request: WeatherRequest, db: Session = Depends(get_db)):
    """Fetch weather data for a given city and date, then store it in the database."""

    # Fetch data from OpenWeatherMap API
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={weather_request.city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")
    
    weather_data = response.json()

    # Extract required data
    temp = weather_data['main']['temp']
    min_temp = weather_data['main']['temp_min']
    max_temp = weather_data['main']['temp_max']
    humidity = weather_data['main']['humidity']

    # Store data in the database
    create_weather_data(db, weather_request.city, weather_request.date, min_temp, max_temp, temp, humidity)

    return {"message": "Weather data stored successfully"}

@app.get("/weather")
def fetch_weather_data(city: str, date: date, db: Session = Depends(get_db)):
    """Retrieves the weather data for a particular city on a given date"""
    weather_data = get_weather_data(db, city, date)

    if weather_data is None:
        raise HTTPException(status_code=404, detail="Weather data not found")

    return {
        "city": weather_data.city,
        "date": weather_data.date,
        "min_temp": weather_data.min_temp,
        "max_temp": weather_data.max_temp,
        "avg_temp": weather_data.avg_temp,
        "humidity": weather_data.humidity
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)