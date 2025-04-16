from django.urls import path, include
from . import views

app_name = "trips"


urlpatterns = [
    path('', views.trips_list, name='list'),
    path('new-trip/', views.trip_new, name='new-trip'),
    path('<slug:slug>', views.trip_page, name='page'),
    path('guide-dashboard/', views.guide_dashboard, name='guide-dashboard'),
    path('edit/<slug:slug>/', views.edit_trip, name='edit-trip'),
    path('trip/<slug:slug>/delete/', views.delete_trip, name='delete-trip'),

    path('<slug:slug>/review/', views.add_review, name='add-review'),

    path('my-cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('confirm-bookings/', views.confirm_bookings, name='confirm-bookings'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add-to-cart'),
    path('my-cart/clear/', views.clear_cart, name='clear-cart'),
]