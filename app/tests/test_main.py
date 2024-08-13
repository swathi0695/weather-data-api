from fastapi.testclient import TestClient
from app.main import app
from datetime import date
import pytest
from app.database import Base, engine
from sqlalchemy.orm import Session
from app.crud import create_weather_data

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_weather_data(db):
    response = client.post(
        "/weather",
        json={"city": "London", "date": str(date.today())}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Weather data stored successfully"}

def test_get_weather_data(db):
    # First, create some test data
    session = Session(engine)
    create_weather_data(session, "Paris", date.today(), 15.0, 25.0, 20.0, 60.0)
    session.close()

    # Then, retrieve the data
    response = client.get(f"/weather?city=Paris&date={str(date.today())}")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Paris"
    assert data["min_temp"] == 15.0
    assert data["max_temp"] == 25.0
    assert data["avg_temp"] == 20.0
    assert data["humidity"] == 60.0

def test_get_nonexistent_weather_data(db):
    response = client.get("/weather?city=NonexistentCity&date=2023-01-01")
    assert response.status_code == 404
    assert response.json() == {"detail": "Weather data not found"}