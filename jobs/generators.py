import random
import uuid
from datetime import datetime, timedelta

from jobs.constants import FuelType, Make, Model, Direction, Emergency, Weather, EmergencyStatus

class City:
    """Represents a city with specific coordinates."""
    def __init__(self, name: str, latitude: float, longitude: float) -> None:
        self.name: str = name
        self.latitude: float = latitude
        self.longitude: float = longitude

class Vehicle:
    """Simulates vehicle movement and generates data."""
    def __init__(self, device_id: str, city: City, fuel_type: FuelType.HYBRID) -> None:
        self.device_id = device_id
        self.city = city
        self.latitude = city.latitude
        self.longitude = city.longitude
        self.fuel_type = fuel_type
        self.timestamp = datetime.now()

    def simulate_movement(self):
        self.latitude += random.uniform(-0.001, 0.001)
        self.longitude += random.uniform(-0.001, 0.001)
        self.timestamp += timedelta(seconds=random.randint(30,60))
        return {
            "id": str(uuid.uuid4()),
            "device_id": self.device_id,
            "timestamp": self.timestamp.isoformat(),
            "location": f"{self.latitude}, {self.longitude}",
            "speed": random.uniform(10,40),
            "direction": random.choice(list(Direction)).value,
            "make": random.choice(list(Make)).value,
            "model": random.choice(list(Model)).value,
            "year": random.randint(2015, 2024),
            "fuelType": self.fuel_type
        }

class GPSData:
    """Generates GPS data for a vehicle."""
    @staticmethod
    def generate_data(vehicle: Vehicle):
        return {
            'id': uuid.uuid4(),
            'deviceId': vehicle.device_id,
            'timestamp': vehicle.timestamp.isoformat(),
            'speed': random.uniform(0, 140),  # km/h
            'direction': random.choice(list(Direction)).value,
            'vehicleType': 'private'
        }

class TrafficCameraData:
    """Generates traffic camera snapshot data."""
    @staticmethod
    def generate_data(vehicle: Vehicle, camera_id: str):
        return {
            'id': uuid.uuid4(),
            'deviceId': vehicle.device_id,
            'cameraId': camera_id,
            'timestamp': vehicle.timestamp.isoformat(),
            'location': (vehicle.latitude, vehicle.longitude),
            'snapshot': 'Base64EncodedString'
        }

class WeatherData:
    """Generates weather data."""
    @staticmethod
    def generate_data(vehicle: Vehicle):
        return {
            'id': uuid.uuid4(),
            'deviceId': vehicle.device_id,
            'location': (vehicle.latitude, vehicle.longitude),
            'timestamp': vehicle.timestamp.isoformat(),
            'temperature': random.uniform(-5, 30),
            'weatherCondition': random.choice(list(Weather)).value,
            'precipitation': random.uniform(0, 25),
            'windSpeed': random.uniform(0, 100),
            'humidity': random.randint(0, 100),
            'airQualityIndex': random.uniform(0, 500)
        }

class EmergencyIncidentData:
    """Generates emergency incident data."""
    @staticmethod
    def generate_data(vehicle: Vehicle):
        return {
            'id': uuid.uuid4(),
            'deviceId': vehicle.device_id,
            'incidentId': uuid.uuid4(),
            'type': random.choice(list(Emergency)).value,
            'timestamp': vehicle.timestamp.isoformat(),
            'location': (vehicle.latitude, vehicle.longitude),
            'status': random.choice(list(EmergencyStatus)).value,
            'description': 'Description of the Incident'
        }