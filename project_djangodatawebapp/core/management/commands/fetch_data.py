import requests
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import City, DataRun, WeatherObservation

BASE_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "MADRID": (40.4168, -3.7038),
    "SEVILLA": (37.3891, -5.9845),
    "BARCELONA": (41.3874, 2.1686),
    "VALENCIA": (39.4699, -0.3763),
    "PONFERRADA": (42.5466, -6.5962),
}


class Command(BaseCommand):
    help = "Fetch current weather data from Open-Meteo and save it to the database"

    def handle(self, *args, **options):
        data_run = DataRun.objects.create(source="api")
        created_count = 0
        updated_count = 0
        skipped_count = 0

        collected_at = timezone.now()

        for city_name, (latitude, longitude) in CITIES.items():
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
            }

            try:
                response = requests.get(BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                current_weather = data.get("current_weather")
                if not current_weather:
                    self.stderr.write(f"No current_weather field found for {city_name}")
                    skipped_count += 1
                    continue

                api_time_raw = current_weather.get("time")
                temperature_c = current_weather.get("temperature")
                windspeed_kmh = current_weather.get("windspeed")

                if (
                    api_time_raw is None
                    or temperature_c is None
                    or windspeed_kmh is None
                ):
                    self.stderr.write(f"Incomplete weather data for {city_name}")
                    skipped_count += 1
                    continue

                api_time = datetime.fromisoformat(api_time_raw)
                api_time = timezone.make_aware(api_time, timezone.get_current_timezone())

                city, _ = City.objects.get_or_create(
                    name=city_name,
                    defaults={
                        "latitude": latitude,
                        "longitude": longitude,
                    },
                )

                observation, created = WeatherObservation.objects.update_or_create(
                    city=city,
                    api_time=api_time,
                    defaults={
                        "data_run": data_run,
                        "collected_at": collected_at,
                        "temperature_c": temperature_c,
                        "windspeed_kmh": windspeed_kmh,
                        "source": "api",
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

                self.stdout.write(f"Fetched weather for {city_name}")

            except requests.exceptions.Timeout:
                self.stderr.write(f"Request timed out for {city_name}")
                skipped_count += 1
            except requests.exceptions.RequestException as exc:
                self.stderr.write(f"Request error for {city_name}: {exc}")
                skipped_count += 1
            except Exception as exc:
                self.stderr.write(f"Unexpected error for {city_name}: {exc}")
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} weather observations"))
        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} weather observations"))
        self.stdout.write(self.style.WARNING(f"Skipped {skipped_count} cities"))