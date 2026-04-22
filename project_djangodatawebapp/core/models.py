from django.db import models
from django.core.validators import MinValueValidator


class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DataRun(models.Model):
    SOURCE_CHOICES = [
        ("csv", "CSV Import"),
        ("api", "API Fetch"),
    ]

    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} run @ {self.created_at:%Y-%m-%d %H:%M}"


class TripRecord(models.Model):
    TRAIN_TYPE_CHOICES = [
        ("AVE", "AVE"),
        ("AV City", "AV City"),
        ("ALVIA", "ALVIA"),
        ("INTERCITY", "INTERCITY"),
        ("EUROMED", "EUROMED"),
        ("REGIONAL", "REGIONAL"),
        ("MD-LD", "MD-LD"),
    ]

    origin = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="departing_trips",
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="arriving_trips",
    )
    data_run = models.ForeignKey(
        DataRun,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    insert_date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    train_type = models.CharField(max_length=30, choices=TRAIN_TYPE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    train_class = models.CharField(max_length=50)
    fare = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]
        unique_together = ["origin", "destination", "start_date", "end_date", "train_type", "fare", "price"]

    def __str__(self):
        return f"{self.origin} → {self.destination} ({self.start_date:%Y-%m-%d %H:%M})"