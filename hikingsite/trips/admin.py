from django.contrib import admin
from .models import Trip, Guide, Booking, Review, Payment, Wishlist, ViewedTrip, ContactMessage, Order, CartItem


# Register your models here.

admin.site.register(Trip)
admin.site.register(Guide)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(Wishlist)
admin.site.register(ViewedTrip)
admin.site.register(ContactMessage)
admin.site.register(Order)
admin.site.register(CartItem)

