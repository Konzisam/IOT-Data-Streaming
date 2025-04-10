import os
import time
import threading
from typing import List

from src.simulation.constants import FuelType
from src.simulation.generators import City, Vehicle, WeatherData, EmergencyIncidentData, TrafficCameraData, GPSData
from src.simulation.kafka_producer import KafkaProducerManager
from src.simulation.utils import ORSClient

# Environment variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')


class VehicleSimulation:
    """Manage the vehicle simulation and parallel production to Kafka"""

    def __init__(self, vehicles: List[Vehicle]) -> None:
        """Initialize simulation with a list of vehicles."""
        self.vehicles = vehicles

    def simulate_journey(self, producer_manager: KafkaProducerManager, vehicle: Vehicle, camera_id: str) -> None:
        """Simulate vehicle journey and generate all data types."""
        while vehicle.route_index < len(vehicle.waypoints) - 1:
            vehicle_data = vehicle.simulate_movement()
            gps_data = GPSData.generate_data(vehicle)
            traffic_camera_data = TrafficCameraData.generate_data(vehicle, camera_id)
            weather_data = WeatherData.generate_data(vehicle)
            emergency_data = EmergencyIncidentData.generate_data(vehicle)

            if vehicle.latitude >= vehicle.end_city.latitude and vehicle.longitude <= vehicle.end_city.longitude:
                print(f"Vehicle has reached {vehicle.end_city.name}. Simulation ended...")
                break

            # Produce data to Kafka for each data type
            producer_manager.produce_data(VEHICLE_TOPIC, vehicle_data)
            producer_manager.produce_data(GPS_TOPIC, gps_data)
            producer_manager.produce_data(TRAFFIC_TOPIC, traffic_camera_data)
            producer_manager.produce_data(WEATHER_TOPIC, weather_data)
            producer_manager.produce_data(EMERGENCY_TOPIC, emergency_data)

            # Simulate time passing
            time.sleep(2)

            all_data = {
                "vehicle_id": vehicle.device_id,
                "vehicle_data": vehicle_data,
                "gps_data": gps_data,
                "traffic_camera_data": traffic_camera_data,
                "weather_data": weather_data,
                "emergency_data": emergency_data
            }

            # print(all_data)

    def start_simulation(self, producer_manager: KafkaProducerManager) -> None:
        """Start the simulation for all vehicles in parallel threads."""
        threads = []
        for vehicle in self.vehicles:
            camera_id = "Camera-Nikon"
            thread = threading.Thread(target=self.simulate_journey, args=(producer_manager, vehicle, camera_id))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


def create_vehicles(ors_client) -> List[Vehicle]:
    """Create and return the list of vehicles for simulation."""
    vehicle1 = Vehicle(
        device_id="V12345",
        start_city=City("Berlin", latitude=52.5200, longitude=13.4050),
        end_city=City("Hamburg", latitude=53.5511, longitude=9.9937),
        fuel_type=FuelType.HYBRID, ors_client=ors_client
    )

    vehicle2 = Vehicle(
        device_id="V67890",
        start_city=City("Osnabrück", latitude=52.2799, longitude=8.0472),
        end_city=City("Hannover", latitude=52.3759, longitude=9.7320),
        fuel_type=FuelType.ELECTRIC, ors_client=ors_client
    )

    vehicle3 = Vehicle(
        device_id="V11223",
        start_city=City("Leipzig", latitude=51.3397, longitude=12.3731),
        end_city=City("Hannover", latitude=52.3759, longitude=9.7320),
        fuel_type=FuelType.DIESEL, ors_client=ors_client
    )

    return [vehicle1, vehicle2, vehicle3]


def main():
    """Main function to initialize and start the simulation."""
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka error: {err}')
    }

    producer_manager = KafkaProducerManager(producer_config)

    ors_client = ORSClient.get_client()

    vehicles = create_vehicles(ors_client)

    try:
        simulation = VehicleSimulation(vehicles)
        simulation.start_simulation(producer_manager)

    except KeyboardInterrupt:
        print('Simulation ended by user')
    except Exception as e:
        print(f'Unexpected error occurred: {e}')


if __name__ == "__main__":
    main()
