from django.shortcuts import render
from . models import Trip

# Create your views here.

def trips_list(request):
    # Dispalys and sorts posts by start date
    trips =Trip.objects.all().order_by('start_date') 
    return render(request, 'trips/trips_list.html', {'trips':trips})

def trip_page(request, slug):
    trip =Trip.objects.get(slug=slug)
    return render(request, 'trips/trip_page.html', {'trip':trip})
