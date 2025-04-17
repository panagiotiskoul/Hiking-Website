from recommender.views import get_recommended_trips, get_top_rated_trips
from django.shortcuts import render, redirect
from trips.forms import ContactMessageForm
from django.contrib import messages



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
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('main:home')
    else:
        form = ContactMessageForm()
    return render(request, 'main/contact.html', {'form': form})