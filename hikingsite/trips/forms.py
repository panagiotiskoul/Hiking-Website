from django import forms
from . import models
from .models import Review


class CreateTrip(forms.ModelForm):
    class Meta:
        model = models.Trip
        fields = ['title', 'location', 'difficulty', 'distance', 
                  'terrain', 'price', 'start_date', 'end_date', 
                  'altitude_difference', 'hiking_duration', 
                  'max_participants', 'description', 'image']
        

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5}))
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
