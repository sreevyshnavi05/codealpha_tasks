from .models import Cart, Wishlist, Category


def cart_context(request):
    cart_count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()

        if cart:
            cart_count = cart.total_items
    except Exception:
        pass
    return {'cart_count': cart_count}


def wishlist_context(request):
    wishlist_count = 0
    try:
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user=request.user).first()
            if wishlist:
                wishlist_count = wishlist.products.count()
    except Exception:
        pass
    return {'wishlist_count': wishlist_count}


def categories_context(request):
    try:
        categories = Category.objects.all()
    except Exception:
        categories = []
    return {'all_categories': categories}
