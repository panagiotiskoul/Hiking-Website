from django.shortcuts import render
from recommender.views import get_recommended_trips, get_top_rated_trips

def home(request):
    if request.user.is_authenticated:
        recommended_trips = get_recommended_trips(request.user)
        if not recommended_trips:
            recommended_trips = get_top_rated_trips()
            section_title = "Top Rated Trips"
        else:
            section_title = "Recommended Trips"
    else:
        recommended_trips = get_top_rated_trips()
        section_title = "Top Rated Trips"

    return render(request, 'main/index.html', {
        'recommended_trips': recommended_trips,
        'section_title': section_title,
    })

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

