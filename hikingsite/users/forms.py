from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data["email"]
    if commit:
        user.save()
    return user


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        disabled=True,  # Make the field uneditable
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


