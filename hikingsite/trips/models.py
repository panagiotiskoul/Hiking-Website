from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.

# Validate that the date is in the future
def validate_future_date(value):
    if value < timezone.now().date():
        raise ValidationError("Date cannot be in the past.")

# Guide Model
class Guide(models.Model):
    EXPERIENCE_CHOICES = [
        ('Amateur', 'Amateur'),
        ('Professional', 'Professional'),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    bio = models.TextField(blank=True, null=True)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# Trip Model
class Trip(models.Model):
    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Hard', 'Hard'),
    ]

    location = models.CharField(max_length=60)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    start_date = models.DateField(validators=[validate_future_date])
    end_date = models.DateField(validators=[validate_future_date])
    description = models.TextField()
    image = models.ImageField(
        upload_to='trip_images/',
        blank=True,
        null=True,
        default='trip_images/default.jpg'
    )
    guide = models.ForeignKey(
        Guide,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trip_guides'
    )
    slug = models.SlugField(unique=True, null=True)

    @property
    def duration(self):
        return (self.end_date - self.start_date).days

    def __str__(self):
        return f"{self.location} ({self.start_date} to {self.end_date})"



# Booking Model
class Booking(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='booked_trips')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookings')
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.trip.location}"



# Review Model
class Review(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.trip.location}"



# Payment Model
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='booking_payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.booking.user.username}"
