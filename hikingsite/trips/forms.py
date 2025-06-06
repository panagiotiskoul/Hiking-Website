from django import forms
from . import models
from .models import Review
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'subject', 'message', 'reason']


class CreateTrip(forms.ModelForm):
    class Meta:
        model = models.Trip
        fields = ['title', 'location', 'difficulty', 'distance', 
                  'terrain', 'price', 'start_date', 'end_date', 
                  'altitude_difference', 'hiking_duration', 
                  'max_participants', 'description', 'image']
        

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={'placeholder': 'Trip Title'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Mount Olympus'}),
            'distance': forms.NumberInput(attrs={'min': 0, 'step': '0.5', 'placeholder': 'Distance in km'}),
            'altitude_difference': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Altitude gain in meters'}),
            'hiking_duration': forms.NumberInput(attrs={'min': 0, 'step': '0.5', 'placeholder': 'Duration in hours'}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': '0.50', 'placeholder': '€'}),
            'max_participants': forms.NumberInput(attrs={'min': 1, 'placeholder': 'e.g. 12'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the trip...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        label="Rating",
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '1',
            'max': '5',
            'step': '1',
            'class': 'form-range small-slider',
            'id': 'id_rating' 
        })
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
