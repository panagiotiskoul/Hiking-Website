from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
        return {'cart_item_count': count}
    return {'cart_item_count': 0}