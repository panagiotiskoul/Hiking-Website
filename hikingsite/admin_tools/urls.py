from django.urls import path
from . import views

app_name = 'admin-tools'

urlpatterns = [
    path('manage-users/', views.manage_users, name='manage-users'),
    path('promote/<int:user_id>/', views.promote_to_guide, name='promote-user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete-user'),
]
