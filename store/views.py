from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.utils import timezone
from decimal import Decimal
import json

from .models import (Category, Product, Cart, CartItem, Wishlist,
                     Order, OrderItem, Coupon, Review,
                     NewsletterSubscription, ContactMessage)
from .forms import ReviewForm, ContactForm, CheckoutForm


# ─────────────────────────── HELPERS ──────────────────────────────

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # Merge session cart into user cart
        if request.session.session_key:
            session_cart = Cart.objects.filter(session_key=request.session.session_key).first()
            if session_cart and session_cart != cart:
                for item in session_cart.items.all():
                    existing = CartItem.objects.filter(cart=cart, product=item.product).first()
                    if existing:
                        existing.quantity += item.quantity
                        existing.save()
                    else:
                        item.cart = cart
                        item.save()
                session_cart.delete()
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


# ─────────────────────────── HOME ─────────────────────────────────

def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    trending_products = Product.objects.filter(is_trending=True, is_active=True)[:8]
    flash_sale_products = Product.objects.filter(is_flash_sale=True, is_active=True)[:6]
    categories = Category.objects.all()

    # Flash sale end time: next 24h from page load (stored in session)
    if 'flash_sale_end' not in request.session:
        end_time = int(timezone.now().timestamp()) + 24 * 3600
        request.session['flash_sale_end'] = end_time
    flash_sale_end = request.session['flash_sale_end']

    context = {
        'featured_products': featured_products,
        'trending_products': trending_products,
        'flash_sale_products': flash_sale_products,
        'categories': categories,
        'flash_sale_end': flash_sale_end,
    }
    return render(request, 'store/home.html', context)


# ─────────────────────────── SHOP ─────────────────────────────────

def shop(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Filters
    search_query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'newest')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    if category_slug:
        products = products.filter(category__slug__iexact=category_slug.strip())

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'best_selling':
        products = products.order_by('-review_count')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    # Track recently viewed
    recently_viewed_ids = request.session.get('recently_viewed', [])
    recently_viewed = Product.objects.filter(id__in=recently_viewed_ids, is_active=True)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    selected_category = None
    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_slug': category_slug,
        'sort_by': sort_by,
        'selected_category': selected_category,
        'total_count': products.count(),
        'recently_viewed': recently_viewed,
    }
    return render(request, 'store/shop.html', context)


# ─────────────────────────── PRODUCT DETAIL ───────────────────────

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or product.rating
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    # Track recently viewed
    recently_viewed = request.session.get('recently_viewed', [])
    if product.id not in recently_viewed:
        recently_viewed.insert(0, product.id)
        request.session['recently_viewed'] = recently_viewed[:6]

    # Wishlist check
    in_wishlist = False
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist and wishlist.products.filter(id=product.id).exists():
            in_wishlist = True

    review_form = ReviewForm()
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            if not user_review:
                rev = review_form.save(commit=False)
                rev.product = product
                rev.user = request.user
                rev.save()
                product.review_count = product.reviews.count()
                product.save()
                messages.success(request, 'Your review has been submitted!')
            else:
                messages.warning(request, 'You have already reviewed this product.')
            return redirect('product_detail', slug=slug)

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'review_form': review_form,
        'user_review': user_review,
        'star_range': range(1, 6),
    }
    return render(request, 'store/product_detail.html', context)


# ─────────────────────────── CART ─────────────────────────────────

def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'message': f'{product.name} added to cart!'
        })
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'shop'))


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    action = request.POST.get('action')
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'remove':
        item.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = get_or_create_cart(request)
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'subtotal': str(cart.subtotal),
        })
    return redirect('cart')


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


def apply_coupon(request):
    code = request.POST.get('coupon_code', '').strip().upper()
    try:
        coupon = Coupon.objects.get(code=code)
        if coupon.is_valid:
            request.session['coupon_code'] = code
            return JsonResponse({'success': True, 'discount': coupon.discount_percent,
                                 'message': f'Coupon applied! {coupon.discount_percent}% off'})
        else:
            return JsonResponse({'success': False, 'message': 'Coupon is expired or invalid.'})
    except Coupon.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid coupon code.'})


# ─────────────────────────── WISHLIST ─────────────────────────────

@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.filter(is_active=True)
    return render(request, 'store/wishlist.html', {'wishlist': wishlist, 'products': products})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if wishlist.products.filter(id=product_id).exists():
        wishlist.products.remove(product)
        in_wishlist = False
        msg = 'Removed from wishlist'
    else:
        wishlist.products.add(product)
        in_wishlist = True
        msg = 'Added to wishlist!'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'in_wishlist': in_wishlist,
                             'wishlist_count': wishlist.products.count(), 'message': msg})
    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'shop'))


# ─────────────────────────── CHECKOUT ─────────────────────────────

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()

    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    subtotal = cart.subtotal
    coupon_code = request.session.get('coupon_code')
    discount = Decimal('0')
    coupon_obj = None

    if coupon_code:
        try:
            coupon_obj = Coupon.objects.get(code=coupon_code, is_active=True)
            if coupon_obj.is_valid:
                discount = subtotal * Decimal(coupon_obj.discount_percent) / 100
        except Coupon.DoesNotExist:
            pass

    shipping = Decimal('0') if subtotal >= Decimal('500') else Decimal('49')
    tax = (subtotal - discount) * Decimal('0.05')
    total = subtotal - discount + shipping + tax

    profile = None
    try:
        profile = request.user.profile
    except Exception:
        pass

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                postal_code=form.cleaned_data['postal_code'],
                payment_method=form.cleaned_data['payment_method'],
                subtotal=subtotal,
                discount=discount,
                shipping=shipping,
                tax=tax,
                total=total,
                coupon=coupon_obj,
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.final_price,
                )
                # Reduce stock
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()

            if coupon_obj:
                coupon_obj.used_count += 1
                coupon_obj.save()

            # Clear cart and coupon
            cart.items.all().delete()
            if 'coupon_code' in request.session:
                del request.session['coupon_code']

            return redirect('order_success', order_id=order.order_id)
    else:
        initial = {}
        if profile:
            initial = {
                'full_name': request.user.get_full_name(),
                'email': request.user.email,
                'phone': profile.phone,
                'address': profile.address,
                'city': profile.city,
                'state': profile.state,
                'postal_code': profile.postal_code,
            }
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'items': items,
        'subtotal': subtotal,
        'discount': discount,
        'shipping': shipping,
        'tax': tax,
        'total': total,
        'coupon_code': coupon_code,
    }
    return render(request, 'store/checkout.html', context)


# ─────────────────────────── ORDERS ───────────────────────────────

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'store/order_history.html', {'orders': orders})


# ─────────────────────────── NEWSLETTER ───────────────────────────

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            _, created = NewsletterSubscription.objects.get_or_create(email=email)
            if created:
                return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})
            return JsonResponse({'success': False, 'message': 'Already subscribed.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})


# ─────────────────────────── ABOUT / CONTACT ──────────────────────

def about(request):
    return render(request, 'store/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent! We\'ll get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'store/contact.html', {'form': form})


# ─────────────────────────── SEARCH ───────────────────────────────

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query),
        is_active=True
    ) if query else Product.objects.none()
    return render(request, 'store/shop.html', {
        'page_obj': Paginator(products, 12).get_page(1),
        'search_query': query,
        'categories': Category.objects.all(),
        'total_count': products.count(),
        'sort_by': 'newest',
    })
