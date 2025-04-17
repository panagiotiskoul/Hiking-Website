from django.urls import path
from . import views

app_name = 'admin-tools'

urlpatterns = [
    path('manage-users/', views.manage_users, name='manage-users'),
    path('promote/<int:user_id>/', views.promote_to_guide, name='promote-user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete-user'),
    path('admin/messages/', views.admin_contact_messages, name='admin-contact-messages'),
    path('admin/messages/<int:message_id>/resolve/', views.mark_message_resolved, name='mark-message-resolved'),
]
