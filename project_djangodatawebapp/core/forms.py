from django import forms
from .models import TripRecord


class TripRecordForm(forms.ModelForm):
    class Meta:
        model = TripRecord
        fields = [
            "origin",
            "destination",
            "insert_date",
            "start_date",
            "end_date",
            "train_type",
            "price",
            "train_class",
            "fare",
        ]