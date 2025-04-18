from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from trips.models import Guide, ContactMessage
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.


# Lets the Admin/superuser view a list of users within the website 
# and promote or delete a user
@login_required(login_url='/users/login/')
def manage_users(request):
    if not request.user.is_superuser:
        raise PermissionDenied  # This triggers 403.html

    users = User.objects.exclude(is_superuser=True)
    guide_user_ids = set(Guide.objects.values_list('user_id', flat=True))
    return render(request, 'admin_tools/manage_users.html', {
        'users': users,
        'guide_user_ids': guide_user_ids
    })



@user_passes_test(lambda u: u.is_superuser)
def promote_to_guide(request, user_id):
    user = get_object_or_404(User, id=user_id)
    guide_group, _ = Group.objects.get_or_create(name='Guides')
    user.groups.add(guide_group)
    Guide.objects.get_or_create(user=user)  # Create guide if doesn't exist
    return redirect('admin-tools:manage-users')



@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin-tools:manage-users')



# Lets the Admin/superuser read messages from within the website and mark the as resolved
@login_required(login_url='/users/login/')
def admin_contact_messages(request):
    if not request.user.is_superuser:
        raise PermissionDenied  # Triggers 403.html

    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_tools/admin_contact_messages.html', {
        'messages_list': messages_list
    })



@require_POST
@user_passes_test(lambda u: u.is_superuser)
def mark_message_resolved(request, message_id):
    message = ContactMessage.objects.get(id=message_id)
    message.is_resolved = True
    message.save()
    return redirect('admin-tools:admin-contact-messages')