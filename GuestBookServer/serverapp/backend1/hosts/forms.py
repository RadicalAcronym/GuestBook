from django import forms
from .models import Event


class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_title', 'event_date', 'event_time']
        widgets = dict(
            event_date=DateInput(
                # format='%Y-%m-%dT%H:%M'
            ),
            event_time=TimeInput(
                # format='H:%M'
            )
        )



