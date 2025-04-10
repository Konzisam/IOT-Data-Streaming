import openrouteservice as ors
from src.config import config

class ORSClient:
    """Singleton client for OpenRouteService API."""
    _client_instance = None

    @classmethod
    def get_client(cls):
        if cls._client_instance is None:
            try:
                api_key = config.configuration.get('OPENROUTE_KEY')
                if not api_key:
                    raise ValueError("API Key for OpenRouteService is missing!")
                cls._client_instance = ors.Client(key=api_key)
                print("OpenRouteService client initialized successfully!")
            except Exception as e:
                print(f"Error initializing OpenRouteService client: {e}")
        return cls._client_instance