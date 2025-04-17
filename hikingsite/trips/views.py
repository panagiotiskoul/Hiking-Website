from django.shortcuts import render, redirect, get_object_or_404
from . models import Trip, Review, ViewedTrip, CartItem, Booking, Order, Payment, Wishlist
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max
from . import forms
from .forms import ReviewForm, CreateTrip
from django.utils import timezone
from django.db.models import Q, Sum
from django.contrib import messages
from django.db import transaction
from decimal import Decimal



# Create your views here.


def trips_list(request):
    difficulty_filter = request.GET.get('difficulty')
    terrain_filter = request.GET.get('terrain')
    max_price_filter = request.GET.get('price')
    max_distance_filter = request.GET.get('distance')

    sort_start_date = request.GET.get('sort_date')
    sort_hiking_time = request.GET.get('sort_hiking_time')

    search_query = request.GET.get('search', '')

    # Get all trips
    trips = Trip.objects.all()

    # Apply search filtering on title, location, and difficulty
    if search_query:
        trips = trips.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(difficulty__icontains=search_query)
        )

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
        'search_query': search_query,
    }

    return render(request, 'trips/trips_list.html', context)




def trip_page(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    user_has_reviewed = False
    in_cart = False
    already_booked = False
    in_wishlist = False 

    if request.user.is_authenticated:
        user = request.user

        # Check if the user has already reviewed this trip
        user_has_reviewed = Review.objects.filter(user=user, trip=trip).exists()

        # Check if it's already in the cart
        in_cart = CartItem.objects.filter(user=user, trip=trip).exists()

        # Check if the user has already booked this trip
        already_booked = Booking.objects.filter(user=user, trip=trip).exists()

        # Check if the user has already saved this trip in whishlist
        in_wishlist = Wishlist.objects.filter(user=user, trip=trip).exists()

        # Save or update the viewed trip
        ViewedTrip.objects.update_or_create(
            user=user,
            trip=trip,
            defaults={'viewed_at': timezone.now()}
        )

    context = {
        'trip': trip,
        'user_has_reviewed': user_has_reviewed,
        'in_cart': in_cart,
        'already_booked': already_booked,
        'in_wishlist': in_wishlist,
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
                newtrip.guide = request.user.guide_profile
            newtrip.save()
            messages.success(request, "New trip created successfully!")
            return redirect('trips:list')
    else:
        form = forms.CreateTrip()

    return render(request, 'trips/trip_new.html', { 'form': form })



@login_required
def edit_trip(request, slug):
    # Make sure this trip belongs to the currently logged-in guide
    trip = get_object_or_404(Trip, slug=slug, guide=request.user.guide_profile)

    if request.method == 'POST':
        form = CreateTrip(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, "Trip information successfully modified!")
            return redirect('trips:page', slug=trip.slug)
    else:
        form = CreateTrip(instance=trip)

    return render(request, 'trips/edit_trip.html', {'form': form, 'trip': trip})


def delete_trip(request, slug):
    trip = get_object_or_404(Trip, slug=slug, guide=request.user.guide_profile)

    if request.method == 'POST':
        trip.delete()
        messages.success(request, "Trip successfully deleted.")
        return redirect('trips:guide-dashboard')

    return render(request, 'trips/confirm_delete.html', {'trip': trip})



@login_required
def guide_dashboard(request):
    if hasattr(request.user, 'guide_profile'):
        trips = Trip.objects.filter(guide=request.user.guide_profile)
    else:
        trips = []
    
    return render(request, 'trips/guide_dashboard.html', {'trips': trips})



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



@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.trip.price for item in cart_items)  # Calculate subtotal
    return render(request, 'trips/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal
    })

@login_required
def add_to_cart(request, slug):
    trip = get_object_or_404(Trip, slug=slug)

    # Prevent duplicates
    if not CartItem.objects.filter(user=request.user, trip=trip).exists():
        CartItem.objects.create(user=request.user, trip=trip)

    return redirect('trips:page', slug=slug)


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('trips:cart')


@login_required
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    return redirect('trips:cart')  # update to the correct trip cart view name


@login_required
def confirm_bookings(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('trips:cart')

    with transaction.atomic():
        # 1. Create a new order
        order = Order.objects.create(user=request.user)

        total_amount = Decimal('0.00')

        # 2. Create bookings and link to the order
        for item in cart_items:
            Booking.objects.create(
                trip=item.trip,
                user=request.user,
                order=order
            )
            total_amount += item.trip.price
            item.delete()

        # 3. Create a payment
        Payment.objects.create(
            order=order,
            amount=total_amount
        )

        messages.success(request, "Your bookings were successfully confirmed and payment completed!")
        return redirect('trips:list')

    return redirect('trips:list')  # or a custom "Thank You" page


@login_required
def add_to_wishlist(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    Wishlist.objects.get_or_create(user=request.user, trip=trip)
    return redirect('trips:page', slug=slug)