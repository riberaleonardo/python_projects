import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Station, DataRun, TripRecord


class Command(BaseCommand):
    help = "Load trip data from CSV into the database"

    def handle(self, *args, **options):
        csv_path = Path("data/raw/reduced_spain_data.csv")

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        data_run = DataRun.objects.create(source="csv")

        created_count = 0
        duplicate_count = 0
        skipped_count = 0

        allowed_types = {
            "AVE",
            "AV City",
            "ALVIA",
            "INTERCITY",
            "EUROMED",
            "REGIONAL",
            "MD-LD",
        }

        def parse_dt(value):
            dt = datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S")
            return timezone.make_aware(dt, timezone.get_current_timezone())

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for i, row in enumerate(reader, start=1):
                try:
                    origin_name = row["origin"].strip()
                    destination_name = row["destination"].strip()
                    insert_date_raw = row["insert_date"].strip()
                    start_date_raw = row["start_date"].strip()
                    end_date_raw = row["end_date"].strip()
                    train_type_raw = row["train_type"].strip()
                    price_raw = row["price"].strip()
                    train_class_raw = row["train_class"].strip()
                    fare_raw = row["fare"].strip()

                    if (
                        not origin_name
                        or not destination_name
                        or not insert_date_raw
                        or not start_date_raw
                        or not end_date_raw
                        or not train_type_raw
                        or not price_raw
                        or not train_class_raw
                        or not fare_raw
                    ):
                        skipped_count += 1
                        continue

                    try:
                        price_value = Decimal(price_raw)
                    except (InvalidOperation, ValueError):
                        skipped_count += 1
                        continue

                    origin_station, _ = Station.objects.get_or_create(name=origin_name)
                    destination_station, _ = Station.objects.get_or_create(name=destination_name)

                    train_type = train_type_raw if train_type_raw in allowed_types else "REGIONAL"

                    insert_date = parse_dt(insert_date_raw)
                    start_date = parse_dt(start_date_raw)
                    end_date = parse_dt(end_date_raw)

                    trip, created = TripRecord.objects.get_or_create(
                        origin=origin_station,
                        destination=destination_station,
                        start_date=start_date,
                        end_date=end_date,
                        train_type=train_type,
                        fare=fare_raw,
                        price=price_value,
                        defaults={
                            "data_run": data_run,
                            "insert_date": insert_date,
                            "train_class": train_class_raw,
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        duplicate_count += 1

                    if i % 1000 == 0:
                        self.stdout.write(
                            f"Processed {i} rows... "
                            f"Created: {created_count}, "
                            f"Duplicates: {duplicate_count}, "
                            f"Skipped: {skipped_count}"
                        )

                except Exception:
                    skipped_count += 1
                    continue

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} trip records"))
        self.stdout.write(self.style.WARNING(f"Skipped {skipped_count} invalid rows"))
        self.stdout.write(self.style.WARNING(f"Skipped {duplicate_count} duplicate rows"))