import requests
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import City, DataRun, WeatherObservation

CURRENT_BASE_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "MADRID": (40.4168, -3.7038),
    "SEVILLA": (37.3891, -5.9845),
    "BARCELONA": (41.3874, 2.1686),
    "VALENCIA": (39.4699, -0.3763),
    "PONFERRADA": (42.5466, -6.5962),
}


class Command(BaseCommand):
    help = "Fetch current weather data and store it"

    def handle(self, *args, **options):
        data_run = DataRun.objects.create(source="api")

        current_created = 0
        current_updated = 0
        historical_created = 0
        skipped_count = 0

        collected_at = timezone.now()


        for city_name, (lat, lon) in CITIES.items():
            city, _ = City.objects.get_or_create(
                name=city_name,
                defaults={"latitude": lat, "longitude": lon},
            )


            # CURRENT WEATHER

            current_params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
            }

            try:
                response = requests.get(CURRENT_BASE_URL, params=current_params, timeout=10)
                response.raise_for_status()
                data = response.json()

                current_weather = data.get("current_weather")
                if current_weather:
                    api_time_raw = current_weather.get("time")
                    temperature_c = current_weather.get("temperature")
                    windspeed_kmh = current_weather.get("windspeed")
                    winddirection_deg = current_weather.get("winddirection")
                    weathercode = current_weather.get("weathercode")
                    is_day = current_weather.get("is_day")

                    if (
                        api_time_raw is not None
                        and temperature_c is not None
                        and windspeed_kmh is not None
                        and winddirection_deg is not None
                        and weathercode is not None
                        and is_day is not None
                    ):
                        api_time = datetime.fromisoformat(api_time_raw)
                        api_time = timezone.make_aware(
                            api_time,
                            timezone.get_current_timezone(),
                        )

                        _, created = WeatherObservation.objects.update_or_create(
                            city=city,
                            api_time=api_time,
                            defaults={
                                "data_run": data_run,
                                "collected_at": collected_at,
                                "temperature_c": temperature_c,
                                "windspeed_kmh": windspeed_kmh,
                                "winddirection_deg": winddirection_deg,
                                "weathercode": weathercode,
                                "is_day": bool(is_day),
                                "source": "api",
                            },
                        )

                        if created:
                            current_created += 1
                        else:
                            current_updated += 1
                else:
                    self.stderr.write(f"No current weather data for {city_name}")
                    skipped_count += 1

            except requests.exceptions.Timeout:
                self.stderr.write(f"Current weather request timed out for {city_name}")
                skipped_count += 1
            except requests.exceptions.RequestException as exc:
                self.stderr.write(f"Current weather request error for {city_name}: {exc}")
                skipped_count += 1
            except Exception as exc:
                self.stderr.write(f"Unexpected current weather error for {city_name}: {exc}")
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {current_created} current weather records"))
        self.stdout.write(self.style.SUCCESS(f"Updated {current_updated} current weather records"))
        self.stdout.write(self.style.WARNING(f"Skipped {skipped_count} requests"))