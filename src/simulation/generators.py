import random
import uuid
from typing import Dict, Union, List
from datetime import datetime, timedelta
from src.simulation.constants import FuelType, Direction, Emergency, Weather, EmergencyStatus, MakeModel
from src.simulation.utils import ORSClient


class City:
    """Represents a city with specific coordinates."""
    def __init__(self, name: str, latitude: float, longitude: float) -> None:
        self.name: str = name
        self.latitude: float = latitude
        self.longitude: float = longitude

class Vehicle:
    """Simulates vehicle movement and generates data."""
    def __init__(self, device_id: str, start_city: City, end_city: City, fuel_type: FuelType, ors_client: ORSClient) -> None:
        self.device_id = device_id
        self.start_city = start_city
        self.end_city = end_city
        self.latitude, self.longitude = start_city.latitude, start_city.longitude
        self.fuel_type = fuel_type
        self.timestamp = datetime.now()
        self.route_index = 0

        self.ors_client = ors_client

        self.waypoints = self.get_route_waypoints()


    def get_route_waypoints(self) -> List[tuple]:
        """Fetches waypoints using OpenRouteService API."""
        coordinates = [(self.start_city.longitude, self.start_city.latitude),
                     (self.end_city.longitude, self.end_city.latitude)]

        route = self.ors_client.directions(
            coordinates=coordinates,
            profile='driving-car',
            format='geojson'
        )

        # Extracting (lat, long) waypoints
        return [(point[1], point[0]) for point in route['features'][0]['geometry']['coordinates']]

    def simulate_movement(self) -> Dict[str, Union[str, float, int]]:
        """Moves the vehicle along waypoints instead of random increments."""
        if self.route_index < len(self.waypoints) - 1:
            self.route_index += 1
            self.latitude, self.longitude = self.waypoints[self.route_index]

        # Add slight variation for realism
        self.latitude += random.uniform(-0.0005, 0.0005)
        self.longitude += random.uniform(-0.0005, 0.0005)
        self.timestamp += timedelta(seconds=random.randint(30, 60))

        make, model = MakeModel.get_random_make_and_model()
        return {
            "id": str(uuid.uuid4()),
            "device_id": self.device_id,
            "timestamp": self.timestamp.isoformat(),
            "location": f"{self.latitude}, {self.longitude}",
            "speed": random.uniform(10, 40),
            "direction": random.choice(list(Direction)).value,
            "make": make,
            "model": model,
            "year": random.randint(2015, 2024),
            "fuelType": self.fuel_type.value
        }

class GPSData:
    """Generates GPS data for a vehicle."""
    @staticmethod
    def generate_data(vehicle: Vehicle) ->Dict:
        return {
            'id': uuid.uuid4(),
            'deviceId': vehicle.device_id,
            'timestamp': vehicle.timestamp.isoformat(),
            'speed': random.uniform(0, 140),  # km/h
            'direction': random.choice(list(Direction)).value,
            'vehicleType': 'private'
        }

class TrafficCameraData:
    """Generate traffic camera snapshot data."""
    @staticmethod
    def generate_data(vehicle: Vehicle, camera_id: str) -> Dict:
        return {
            'id': uuid.uuid4(),
            'deviceId': vehicle.device_id,
            'cameraId': camera_id,
            'timestamp': vehicle.timestamp.isoformat(),
            'location': (vehicle.latitude, vehicle.longitude),
            'snapshot': 'Base64EncodedString'
        }

class WeatherData:
    """Generate weather data."""
    @staticmethod
    def generate_data(vehicle: Vehicle) -> Dict:
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
    """Generate emergency incident data."""
    @staticmethod
    def generate_data(vehicle: Vehicle) -> Dict:
        return {
            'id': uuid.uuid4(),
            'deviceId': vehicle.device_id,
            'incidentId': uuid.uuid4(),
            'type': random.choice(list(Emergency)).value,
            'timestamp': vehicle.timestamp.isoformat(),
            'location': (vehicle.latitude, vehicle.longitude),
            'status': random.choice(list(EmergencyStatus)).value,
            'description': 'Further description of the incident'
        }