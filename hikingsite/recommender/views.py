from django.shortcuts import render
from collections import Counter
from django.db.models import Q
from trips.models import Trip, Wishlist, Booking, ViewedTrip
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

# Create your views here.

def get_recommended_trips(user, max_recommendations=4):
    # Step 1: Gather interacted trips
    wishlisted = Trip.objects.filter(wishlisted_by__user=user)
    booked = Trip.objects.filter(booked_trips__user=user)
    viewed_trip_entries = ViewedTrip.objects.filter(user=user).order_by('-viewed_at')[:10]
    viewed = [entry.trip for entry in viewed_trip_entries]


    # Modify this to exclude from recomendations trips you have already seen
    # To do this use this code instead :interacted_trips = set(wishlisted) | set(booked) | set(viewed)
    interacted_trips = set(wishlisted) | set(booked)

    # Step 2: Build preference profiles
    terrain_pref = Counter([trip.terrain for trip in interacted_trips])
    difficulty_pref = Counter([trip.difficulty for trip in interacted_trips])

    # Step 3: Filter out trips already interacted with
    candidate_trips = Trip.objects.exclude(
        Q(id__in=[trip.id for trip in interacted_trips])
    )

    # Step 4: Score trips based on matching features
    scored_trips = []
    for trip in candidate_trips:
        score = 0
        score += terrain_pref[trip.terrain] * 2  # Terrain is weighted more
        score += difficulty_pref[trip.difficulty]  # Difficulty is secondary
        scored_trips.append((trip, score))

    # Step 5: Sort and return top N
    scored_trips.sort(key=lambda x: x[1], reverse=True)
    return [trip for trip, score in scored_trips[:max_recommendations]]



def get_top_rated_trips(limit=3):
    return Trip.objects.annotate(avg_rating=Avg('trip_reviews__rating')) \
                       .filter(avg_rating__isnull=False) \
                       .order_by('-avg_rating')[:limit]


@login_required
def recommended_view(request):
    if request.user.is_authenticated:
        recommended_trips = get_recommended_trips(request.user)
        if not recommended_trips:
            recommended_trips = get_top_rated_trips()
    else:
        recommended_trips = get_top_rated_trips()

    return render(request, 'recommender/recommended.html', {
        'recommended_trips': recommended_trips
    })
