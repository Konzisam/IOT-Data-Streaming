from enum import Enum

class FuelType(Enum):
    """Enum for vehicle fuel types."""
    HYBRID = "Hybrid"
    ELECTRIC = "Electric"
    GASOLINE = "Gasoline"
    DIESEL = "Diesel"

class Direction(Enum):
    """Enum for possible movement directions."""
    NORTH_EAST = "North-East"
    SOUTH_WEST = "South-West"
    NORTH_WEST = "North-West"
    SOUTH_EAST = "South-East"


class Make(Enum):
    """Enum for vehicle makes."""
    TOYOTA = "Toyota"
    FORD = "Ford"
    BMW = "BMW"
    HONDA = "Honda"
    CHEVROLET = "Chevrolet"

class Model(Enum):
    """Enum for vehicle models."""
    PRIUS = "Prius"
    FOCUS = "Focus"
    X5 = "X5"
    CIVIC = "Civic"
    MALIBU = "Malibu"

class Weather(Enum):
    """Enum for the weather conditions"""
    CLOUDY = "Cloudy"
    SUNNY = "Sunny"
    RAINY = "Rainy"
    SNOWING = "Snowing"

class Emergency(Enum):
    """Enum for the Emergency conditions"""
    ACCIDENT = "Accident"
    FIRE = "Fire"
    MEDICAL = "Medical"
    POLICE = "Police"
    NONE = "None"

class EmergencyStatus(Enum):
    """Enum for Emergency status conditions"""
    ACTIVE = "Active"
    RESOLVED = "Resolved"