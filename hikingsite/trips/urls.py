from django.urls import path, include
from . import views

app_name = "trips"


urlpatterns = [
    path('', views.trips_list, name='list'),
    path('<slug:slug>', views.trip_page, name='page'),
]