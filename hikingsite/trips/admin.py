from django.contrib import admin
from .models import Guide, Trip, Booking, Review, Payment

# Register your models here.

admin.site.register(Guide)
admin.site.register(Trip)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Payment)
