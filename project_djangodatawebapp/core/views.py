import json
import numpy as np
import pandas as pd

from io import StringIO

from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TripRecordForm
from .models import TripRecord, WeatherObservation


def home(request):
    trip_count = TripRecord.objects.count()
    recent_trips = TripRecord.objects.select_related("origin", "destination").all()[:5]

    context = {
        "trip_count": trip_count,
        "recent_trips": recent_trips,
    }
    return render(request, "core/home.html", context)


def record_list(request):
    records = TripRecord.objects.select_related("origin", "destination").all()
    paginator = Paginator(records, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "core/list.html", {"page_obj": page_obj})

def record_detail(request, pk):
    record = get_object_or_404(
        TripRecord.objects.select_related("origin", "destination"),
        pk=pk,
    )

    current_origin_weather = WeatherObservation.objects.filter(
        city__name__iexact=record.origin.name
    ).order_by("-api_time").first()

    current_destination_weather = WeatherObservation.objects.filter(
        city__name__iexact=record.destination.name
    ).order_by("-api_time").first()

    return render(
        request,
        "core/detail.html",
        {
            "record": record,
            "current_origin_weather": current_origin_weather,
            "current_destination_weather": current_destination_weather,
        },
    )


def record_add(request):
    if request.method == "POST":
        form = TripRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            return redirect("record_detail", pk=record.pk)
    else:
        form = TripRecordForm()

    return render(
        request,
        "core/form.html",
        {
            "form": form,
            "title": "Add Trip Record",
            "submit_text": "Create Record",
        },
    )


def record_edit(request, pk):
    record = get_object_or_404(TripRecord, pk=pk)

    if request.method == "POST":
        form = TripRecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save()
            return redirect("record_detail", pk=record.pk)
    else:
        form = TripRecordForm(instance=record)

    return render(
        request,
        "core/form.html",
        {
            "form": form,
            "title": "Edit Trip Record",
            "submit_text": "Save Changes",
        },
    )


def record_delete(request, pk):
    record = get_object_or_404(TripRecord, pk=pk)

    if request.method == "POST":
        record.delete()
        return redirect("record_list")

    return render(request, "core/confirm_delete.html", {"record": record})


def analytics(request):
    qs = TripRecord.objects.values(
        "start_date",
        "end_date",
        "train_type",
        "price",
    )

    df = pd.DataFrame(list(qs))

    if df.empty:
        context = {
            "chart_one_json": json.dumps({
                "type": "bar",
                "labels": [],
                "datasets": [{"label": "Trips by Hour", "data": []}],
            }),
            "chart_two_json": json.dumps({
                "type": "doughnut",
                "labels": [],
                "datasets": [{"label": "Average Trip Duration", "data": []}],
            }),
            "summary_rows": [],
        }
        return render(request, "core/analytics.html", context)

    # Parse datetimes
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

    # Drop rows missing required dates
    df = df.dropna(subset=["start_date", "end_date"])

    # Derive hour from start_date
    df["hour"] = df["start_date"].dt.hour

    # Compute trip duration in hours
    df["trip_duration_hours"] = (
        (df["end_date"] - df["start_date"]).dt.total_seconds() / 3600
    )

    # Clean numeric fields
    df["trip_duration_hours"] = pd.to_numeric(df["trip_duration_hours"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    #chart 1
    hour_counts = df.groupby("hour").size().sort_index()

    chart_one = {
        "type": "bar",
        "labels": [str(x) for x in hour_counts.index.tolist()],
        "datasets": [
            {
                "label": "Trips by Hour",
                "data": hour_counts.values.tolist(),
            }
        ],
    }

#   chart 2
    duration_by_train_type = (
        df.dropna(subset=["train_type", "trip_duration_hours"])
          .groupby("train_type")["trip_duration_hours"]
          .mean()
          .sort_values(ascending=False)
    )

    chart_two = {
        "type": "doughnut",
        "labels": duration_by_train_type.index.tolist(),
        "datasets": [
            {
                "label": "Average Trip Duration (Hours)",
                "data": [round(x, 2) for x in duration_by_train_type.values.tolist()],
            }
        ],
    }

# summarize tables
    duration_series = df["trip_duration_hours"].dropna()
    price_series = df["price"].dropna()

    summary_rows = [
        {
            "field": "Trip Duration (Hours)",
            "count": int(duration_series.count()),
            "mean": round(float(duration_series.mean()), 2),
            "min": round(float(duration_series.min()), 2),
            "max": round(float(duration_series.max()), 2),
        },
        {
            "field": "Price",
            "count": int(price_series.count()),
            "mean": round(float(price_series.mean()), 2),
            "min": round(float(price_series.min()), 2),
            "max": round(float(price_series.max()), 2),
        },
    ]

    context = {
        "chart_one_json": json.dumps(chart_one),
        "chart_two_json": json.dumps(chart_two),
        "summary_rows": summary_rows,
    }
    return render(request, "core/analytics.html", context)
@staff_member_required
def fetch_data_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    output = StringIO()
    call_command("fetch_data", stdout=output)

    return render(
        request,
        "core/fetch_result.html",
        {"command_output": output.getvalue()},
    )


def custom_404(request, exception):
    return render(request, "core/404.html", status=404)
