from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/coupon/', views.apply_coupon, name='apply_coupon'),

    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<uuid:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.order_history, name='order_history'),

    # Other
    path('newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
