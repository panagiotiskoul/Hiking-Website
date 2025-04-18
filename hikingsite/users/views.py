from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserUpdateForm
from trips.models import Payment, Wishlist, Review, ViewedTrip, Trip, Booking
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from django.core.exceptions import PermissionDenied

# Create your views here.

#------------------------
# Register, Login, Logout
#------------------------


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("trips:list")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", { "form":form })



def login_view(request):
    if request.method == "POST":
        form =AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("trips:list")

    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form":form })



def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("main:home")
    else:
        # Always return something
        return redirect("main:home")



#-------------------------
# My Account Functionality
#-------------------------


@login_required
def account_info(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your information has been updated successfully!")
            return redirect('main:home')  # Reload the page after saving
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/account_info.html', {'form': form})



class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users:account-info')  # redirect to your account info

    def form_valid(self, form):
        messages.success(self.request, 'Your password was changed successfully.')
        return super().form_valid(form)



@login_required
def my_payments(request):
    payments = Payment.objects.filter(order__user=request.user).select_related('order').prefetch_related('order__bookings__trip')
    return render(request, 'users/my_payments.html', {'payments': payments})



@login_required
def my_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('trip')
    return render(request, 'users/my_wishlist.html', {'wishlist_items': wishlist_items})



@require_POST
@login_required
def remove_from_wishlist(request, trip_id):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, trip_id=trip_id)
    wishlist_item.delete()
    return redirect('users:account-wishlist')



@login_required
def user_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related('trip').order_by('-created_at')
    return render(request, 'users/user_reviews.html', {'reviews': reviews})



@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('users:user-reviews')



@login_required
def my_activity(request):
    recent_views = ViewedTrip.objects.filter(user=request.user).order_by('-viewed_at')[:10]
    return render(request, 'users/my_activity.html', {'recent_views': recent_views})



#-------------------------------
# Pages Only accesible to Guides
#-------------------------------


def is_guide(user):
    return hasattr(user, 'guide_profile')

@login_required(login_url="/users/login/")
def all_booked_trips_view(request):
    if not is_guide(request.user):
        raise PermissionDenied  # Shows your 403.html page if it exists

    trips_with_bookings = Trip.objects.filter(
        booked_trips__isnull=False
    ).distinct().prefetch_related('booked_trips__user')

    return render(request, 'users/all_booked_trips.html', {
        'trips': trips_with_bookings
    })