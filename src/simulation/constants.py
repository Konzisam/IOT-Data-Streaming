from enum import Enum
import random

class MakeModel(Enum):
    """Enum for vehicle makes and their corresponding models."""
    TOYOTA = ["Prius", "Corolla", "Camry", "Rav4"]
    FORD = ["Focus", "F-150", "Mustang", "Escape"]
    BMW = ["X5", "X3", "M3", "320i"]
    HONDA = ["Civic", "Accord", "CR-V", "Fit"]
    CHEVROLET = ["Malibu", "Silverado", "Tahoe", "Impala"]

    @staticmethod
    def get_random_make_and_model():
        make = random.choice(list(MakeModel))
        model = random.choice(make.value)
        return make.name, model


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

