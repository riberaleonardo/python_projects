from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Model 1: City
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


# Model 2: DataRun (tracks CSV vs API imports)
class DataRun(models.Model):
    SOURCE_CHOICES = [
        ('csv', 'CSV Import'),
        ('api', 'API Fetch'),
    ]

    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} run @ {self.created_at.strftime('%Y-%m-%d %H:%M')}"


# Model 3: WeatherRecord
class WeatherRecord(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='records')
    data_run = models.ForeignKey(DataRun, on_delete=models.SET_NULL, null=True, blank=True)

    record_time = models.DateTimeField()

    temperature_c = models.FloatField()
    windspeed_kmh = models.FloatField(validators=[MinValueValidator(0)])
    winddirection_deg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(360)]
    )

    weathercode = models.IntegerField()
    is_day = models.BooleanField()

    source = models.CharField(
        max_length=10,
        choices=[('csv', 'CSV Import'), ('api', 'API Fetch')]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-record_time']
        unique_together = ['city', 'record_time', 'source']

    def __str__(self):
        return f"{self.city.name} @ {self.record_time}"