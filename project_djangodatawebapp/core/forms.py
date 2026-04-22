from django import forms
from .models import TripRecord


class TripRecordForm(forms.ModelForm):
    class Meta:
        model = TripRecord
        fields = "__all__"