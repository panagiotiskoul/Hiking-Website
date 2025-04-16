from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordChangeView

app_name = "users"


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/info/', views.account_info, name='account-info'),
    path('my-payments/', views.my_payments, name='my-payments'),
    path('account/wishlist/', views.my_wishlist, name='account-wishlist'),
    path('account/wishlist/remove/<int:trip_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('account/reviews/', views.user_reviews, name='user-reviews'),
    path('account/reviews/delete/<int:review_id>/', views.delete_review, name='delete-review'),
    path('account/activity/', views.my_activity, name='account-activity'),
    path('account/change-password/', CustomPasswordChangeView.as_view(), name='change-password'),
    path('admin/messages/', views.admin_contact_messages, name='admin-contact-messages'),
    path('admin/messages/<int:message_id>/resolve/', views.mark_message_resolved, name='mark-message-resolved'),


]