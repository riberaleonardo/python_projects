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