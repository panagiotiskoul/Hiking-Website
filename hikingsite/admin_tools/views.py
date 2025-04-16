from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from trips.models import Guide


# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
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