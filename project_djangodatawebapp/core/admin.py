from django.contrib import admin
from .models import Station, DataRun, TripRecord, City, WeatherObservation


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(DataRun)
class DataRunAdmin(admin.ModelAdmin):
    list_display = ("source", "created_at")
    list_filter = ("source",)


@admin.register(TripRecord)
class TripRecordAdmin(admin.ModelAdmin):
    list_display = (
        "origin",
        "destination",
        "start_date",
        "end_date",
        "train_type",
        "price",
        "train_class",
        "fare",
    )
    list_filter = ("train_type", "train_class", "fare", "origin", "destination")
    search_fields = ("origin__name", "destination__name")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("name",)


@admin.register(WeatherObservation)
class WeatherObservationAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "api_time",
        "temperature_c",
        "windspeed_kmh",
        "weathercode",
        "is_day",
        "source",
    )
    list_filter = ("city", "source", "is_day")
    search_fields = ("city__name",)