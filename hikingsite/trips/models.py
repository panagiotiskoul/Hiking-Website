from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify




# Create your models here.

# Validate that the date is in the future
def validate_future_date(value):
    if value < timezone.now().date():
        raise ValidationError("Date cannot be in the past.")



# Trip Model
class Trip(models.Model):
    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Hard', 'Hard'),
        ('Extreme', 'Extreme')
    ]

    TERRAIN_TYPES = [
        ('Forest', 'Forest'),
        ('Mountain', 'Mountain'),
        ('Beach', 'Beach'),
        ('Urban', 'Urban'),
    ]

    title = models.CharField(max_length=60, unique=True)
    location = models.CharField(max_length=40)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    distance = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    terrain = models.CharField(max_length=20, choices=TERRAIN_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    start_date = models.DateField(validators=[validate_future_date])
    end_date = models.DateField(validators=[validate_future_date])
    altitude_difference = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    hiking_duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    max_participants = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    description = models.TextField(max_length=500)
    image = models.ImageField(default='default.png', blank=True, null=True)

    guide = models.ForeignKey('Guide', on_delete=models.SET_NULL, null=True, blank=True, related_name='trip_guides'
    )

    slug = models.SlugField(unique=True, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': "End date must be after the start date."})

    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.title} - {self.location} ({self.start_date} to {self.end_date})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="orders",)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class Booking(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='booked_trips')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookings')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.trip.title}"
    


# Guide Model
class Guide(models.Model):
    EXPERIENCE_CHOICES = [
        ('Amateur', 'Amateur'),
        ('Professional', 'Professional'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="guide_profile", null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, default='Not Provided')
    bio = models.TextField(blank=True, null=True, default='Not Provided')
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, blank=True, default='Amateur')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}" if self.user else "Unnamed Guide"



# Review Model
class Review(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'trip')

    def __str__(self):
        return f"Review by {self.user.username} on {self.trip.location}"



class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} by {self.order.user.username}"
    


# Views History Model
class ViewedTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_trips')
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name='viewed_by')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'trip')

    def __str__(self):
        return f"{self.user.username} viewed {self.trip.title}"
    


# Wishlist Model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} added {self.trip.title} to wishlist"
    


# Contact Form Model
class ContactMessage(models.Model):
    REASON_CHOICES = [
        ("Upcoming trip", "Upcoming trip"),
        ("Past trip", "Past trip"),
        ("Trip suggestion", "Trip suggestion"),
        ("Shop", "Shop"),
        ("Payment issue", "Payment issue"),
        ("Account issue", "Account issue"),
        ("Other", "Other"),
    ]

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    subject = models.CharField(max_length=40)
    message = models.TextField(max_length=500)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.first_name} {self.last_name} ({self.email})"
    

# Shopping Cart Model
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='carted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'trip')

    def __str__(self):
        return f"{self.user.username} - {self.trip.title}"



