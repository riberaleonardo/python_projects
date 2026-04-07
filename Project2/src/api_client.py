import logging
from typing import Dict, Optional

import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_current_weather(city: str, latitude: float, longitude: float, timeout: int = 10) -> Optional[Dict]:
    """Fetch current weather data for a single city from Open-Meteo."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        current_weather = data.get("current_weather")
        if not current_weather:
            logging.warning("No current_weather field found for %s", city)
            return None

        record = {
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
            "temperature_c": current_weather.get("temperature"),
            "windspeed_kmh": current_weather.get("windspeed"),
            "winddirection_deg": current_weather.get("winddirection"),
            "weathercode": current_weather.get("weathercode"),
            "is_day": current_weather.get("is_day"),
            "api_time": current_weather.get("time"),
        }
        return record

    except requests.exceptions.Timeout:
        logging.error("Request timed out for %s", city)
        return None
    except requests.exceptions.RequestException as exc:
        logging.error("Request error for %s: %s", city, exc)
        return None