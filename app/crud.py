from sqlalchemy.orm import Session
from .database import WeatherData
from datetime import date

def create_weather_data(db: Session, city: str, date: date, min_temp: float, max_temp: float, avg_temp: float, humidity: float):
    """Stores the data into DB"""
    db_weather = WeatherData(
        city=city,
        date=date,
        min_temp=min_temp,
        max_temp=max_temp,
        avg_temp=avg_temp,
        humidity=humidity
    )
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather

def get_weather_data(db: Session, city: str, date: date):
    """Queries the DB for weather data"""
    return db.query(WeatherData).filter(WeatherData.city == city, WeatherData.date == date).first()