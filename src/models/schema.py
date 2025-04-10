from typing import Optional, Tuple, Union, Dict, Type
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class VehicleModel(BaseModel):
    id: UUID
    device_id: str
    timestamp: datetime
    location: str  # e.g., "52.5200, 13.4050"
    speed: float
    direction: str
    make: str
    model: str
    year: int
    fuelType: str


class GPSModel(BaseModel):
    id: UUID
    deviceId: str
    timestamp: datetime
    speed: float
    direction: str
    vehicleType: str

class TrafficModel(BaseModel):
    id: UUID
    deviceId: str
    cameraId: str
    timestamp: datetime
    location: Tuple[float, float]  # (lat, lon)
    snapshot: str


class WeatherModel(BaseModel):
    id: UUID
    deviceId: str
    location: Tuple[float, float]
    timestamp: datetime
    temperature: float
    weatherCondition: str
    precipitation: float
    windSpeed: float
    humidity: int
    airQualityIndex: float


class EmergencyModel(BaseModel):
    id: UUID
    deviceId: str
    incidentId: UUID
    type: str
    timestamp: datetime
    location: Tuple[float, float]
    status: str
    description: str


class SchemaManager:
    schemas: Dict[str, Type[BaseModel]] = {
        "vehicle_schema": VehicleModel,
        "gps_schema": GPSModel,
        "traffic_schema": TrafficModel,
        "weather_schema": WeatherModel,
        "emergency_schema": EmergencyModel
    }

    @classmethod
    def get_schema(cls, topic: str) -> Optional[Type[BaseModel]]:
        return cls.schemas.get(topic)