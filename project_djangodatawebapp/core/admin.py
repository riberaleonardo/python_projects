from django.contrib import admin
from .models import City, DataRun, WeatherRecord


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("name",)


@admin.register(DataRun)
class DataRunAdmin(admin.ModelAdmin):
    list_display = ("source", "created_at")
    list_filter = ("source",)


@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ("city", "record_time", "temperature_c", "windspeed_kmh", "source")
    list_filter = ("city", "source")
    search_fields = ("city__name",)