import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.simulation.generators import Vehicle, City, FuelType
from src.simulation.utils import ORSClient


# Fixture to mock ORSClient
@pytest.fixture
def mock_ors_client():
    """
    Fixture to mock ORSClient and return a mock instance.
    """
    mock_client = MagicMock()

    # Simulate the behavior of the directions method
    mock_client.directions.return_value = {
        'features': [{
            'geometry': {
                'coordinates': [
                    (13.0645, 52.3906),
                    (12.3731, 51.3397)
                ]
            }
        }]
    }

    # Patch ORSClient.get_client to return the mock_client
    with patch.object(ORSClient, 'get_client', return_value=mock_client):
        yield mock_client


# Fixture to create a Vehicle instance with the mocked ORSClient
@pytest.fixture
def vehicle(mock_ors_client):
    """
    Fixture to create a Vehicle instance with a mock ORSClient.
    """
    start_city = City("Potsdam", 52.3906, 13.0645)
    end_city = City("Leipzig", 51.3397, 12.3731)
    return Vehicle("V12345", start_city, end_city, FuelType.HYBRID, mock_ors_client)


# Test vehicle initialization and waypoints generation
def test_vehicle_initialization_and_waypoints(vehicle, mock_ors_client):
    """
    Test that a Vehicle is initialized with correct attributes and waypoints are generated correctly.
    """
    # Check attributes of the Vehicle instance
    assert vehicle.device_id == "V12345"
    assert vehicle.start_city.name == "Potsdam"
    assert vehicle.end_city.name == "Leipzig"
    assert isinstance(vehicle.timestamp, datetime)

    # Verify the ORSClient directions method is called correctly
    mock_ors_client.directions.assert_called_once_with(
        coordinates=[(13.0645, 52.3906), (12.3731, 51.3397)],
        profile='driving-car',
        format='geojson'
    )

    # Verify that the waypoints are set correctly
    expected_waypoints = [(52.3906, 13.0645), (51.3397, 12.3731)]
    assert vehicle.waypoints == expected_waypoints

# Test vehicle movement simulation
def test_simulate_movement(vehicle):
    """
    Test that the vehicle moves and updates location correctly.
    """
    initial_location = (vehicle.latitude, vehicle.longitude)
    initial_timestamp = vehicle.timestamp

    # Simulate movement
    vehicle.simulate_movement()

    # Check that the vehicle's location and timestamp were updated
    assert (vehicle.latitude, vehicle.longitude) != initial_location
    assert vehicle.timestamp > initial_timestamp
