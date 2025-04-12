from django.urls import path, include
from . import views

app_name = "trips"


urlpatterns = [
    path('', views.trips_list, name='list'),
    path('new-trip/', views.trip_new, name='new-trip'),
    path('<slug:slug>', views.trip_page, name='page'),
]