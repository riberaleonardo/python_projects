from datetime import datetime
import logging
from pathlib import Path

import pandas as pd

from api_client import fetch_current_weather
from storage import append_to_csv, append_to_sqlite, ensure_directories

CITIES = {
    "Tallahassee": (30.4383, -84.2807),
    "Miami": (25.7617, -80.1918),
    "Orlando": (28.5383, -81.3792),
    "Tampa": (27.9506, -82.4572),
    "Jacksonville": (30.3322, -81.6557),
}



def configure_logging(log_file: Path) -> None:
    """Configure file and console logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )



def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    ensure_directories(project_root)

    log_file = project_root / "logs" / "pipeline.log"
    configure_logging(log_file)

    csv_path = project_root / "data" / "processed" / "weather_data.csv"
    db_path = project_root / "data" / "processed" / "weather_data.sqlite"

    records = []
    collected_at = datetime.now().isoformat(timespec="seconds")

    for city, (latitude, longitude) in CITIES.items():
        print(f"Fetching weather data for {city}...")
        logging.info("Fetching weather data for %s", city)

        record = fetch_current_weather(city, latitude, longitude)
        if record is None:
            continue

        record["collected_at"] = collected_at
        records.append(record)

    if not records:
        logging.warning("No records collected during this run.")
        print("No records collected during this run.")
        return

    df = pd.DataFrame(records)
    append_to_csv(df, csv_path)
    append_to_sqlite(df, db_path)

    logging.info("Saved %d records to CSV and SQLite.", len(df))
    print(f"Saved {len(df)} records to CSV and SQLite.")



if __name__ == "__main__":
    main()