from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from trips.models import Payment, Wishlist, Review, ViewedTrip
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

# Create your views here.


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


@login_required
def account_info(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main:home')  # Reload the page after saving
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/account_info.html', {'form': form})

@login_required
def my_payments(request):
    payments = Payment.objects.filter(order__bookings__user=request.user).select_related(
        'order').prefetch_related('order__bookings__trip').distinct()
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

