from django import forms
from . import models


class CreateTrip(forms.ModelForm):
    class Meta:
        model = models.Trip
        fields = ['title', 'location', 'difficulty', 'distance', 
                  'terrain', 'price', 'start_date', 'end_date', 
                  'altitude_difference', 'hiking_duration', 
                  'max_participants', 'description', 'image']