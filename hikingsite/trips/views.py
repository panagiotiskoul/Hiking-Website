from django.shortcuts import render, redirect, get_object_or_404
from . models import Trip, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max
from . import forms
from .forms import ReviewForm

# Create your views here.


def trips_list(request):
    difficulty_filter = request.GET.get('difficulty')
    terrain_filter = request.GET.get('terrain')
    max_price_filter = request.GET.get('price')
    max_distance_filter = request.GET.get('distance')

    sort_start_date = request.GET.get('sort_date')
    sort_hiking_time = request.GET.get('sort_hiking_time')

    # Get all trips
    trips = Trip.objects.all()

    # Get min/max price range
    price_range = trips.aggregate(Min('price'), Max('price'))
    min_price = price_range['price__min'] or 0
    max_price = price_range['price__max'] or 1000

    # Get min/max distance range
    distance_range = trips.aggregate(Min('distance'), Max('distance'))
    min_distance = distance_range['distance__min'] or 0
    max_distance = distance_range['distance__max'] or 100

    # Apply filters
    if difficulty_filter:
        trips = trips.filter(difficulty=difficulty_filter)

    if terrain_filter:
        trips = trips.filter(terrain=terrain_filter)

    if max_price_filter:
        try:
            trips = trips.filter(price__lte=float(max_price_filter))
        except ValueError:
            pass

    if max_distance_filter:
        try:
            trips = trips.filter(distance__lte=float(max_distance_filter))
        except ValueError:
            pass

    # Handle sorting
    if sort_hiking_time:
        trips = trips.order_by('hiking_duration' if sort_hiking_time == 'asc' else '-hiking_duration')
    elif sort_start_date:
        trips = trips.order_by('start_date' if sort_start_date == 'asc' else '-start_date')
    else:
        trips = trips.order_by('start_date')

    context = {
        'trips': trips,
        'difficulty_filter': difficulty_filter,
        'terrain_filter': terrain_filter,
        'sort_start_date': sort_start_date,
        'sort_hiking_time': sort_hiking_time,
        'min_price': int(min_price),
        'max_price': int(max_price),
        'current_price': float(max_price_filter) if max_price_filter else int(max_price),
        'min_distance': float(min_distance),
        'max_distance': float(max_distance),
        'current_distance': float(max_distance_filter) if max_distance_filter else float(max_distance),
    }

    return render(request, 'trips/trips_list.html', context)




def trip_page(request, slug):
    trip = Trip.objects.get(slug=slug)
    user_has_reviewed = False

    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(user=request.user, trip=trip).exists()

    context = {
        'trip': trip,
        'user_has_reviewed': user_has_reviewed
    }

    return render(request, 'trips/trip_page.html', context)



@login_required(login_url="/users/login/")
def trip_new(request):
    if request.method == 'POST':
        form = forms.CreateTrip(request.POST, request.FILES)
        if form.is_valid():
            newtrip = form.save(commit=False)
            # Automatically assign the logged-in guide
            if hasattr(request.user, 'guide_profile'):
                print("Guide profile exists:", request.user.guide_profile) #debug print
                newtrip.guide = request.user.guide_profile
            else:
                print("No guide profile found for user:", request.user.username) #debug print
            newtrip.save()
            return redirect('trips:list')
    else:
        form = forms.CreateTrip()

    return render(request, 'trips/trip_new.html', { 'form': form })




@login_required
def add_review(request, slug):
    trip = get_object_or_404(Trip, slug=slug)

    existing_review = Review.objects.filter(user=request.user, trip=trip).first()
    if existing_review:
        return redirect('trips:page', slug=slug)  # Redirect if review already exists

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.trip = trip
            review.user = request.user
            review.save()
            return redirect('trips:page', slug=slug)
    else:
        form = ReviewForm()

    return render(request, 'trips/add_review.html', {'form': form, 'trip': trip})