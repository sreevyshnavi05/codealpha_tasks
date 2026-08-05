from django.contrib import admin
from .models import (Category, Product, ProductImage, Review,
                     Cart, CartItem, Wishlist, Order, OrderItem,
                     Coupon, NewsletterSubscription, ContactMessage)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['user', 'rating', 'comment', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'discount_price', 'stock',
                    'is_featured', 'is_trending', 'is_flash_sale', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_trending', 'is_flash_sale', 'is_active']
    search_fields = ['name', 'brand', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_trending', 'is_flash_sale', 'is_active', 'stock']
    inlines = [ProductImageInline, ReviewInline]
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'slug', 'category', 'brand', 'image')}),
        ('Pricing', {'fields': ('price', 'discount_price')}),
        ('Details', {'fields': ('description', 'features', 'specifications', 'stock')}),
        ('Ratings', {'fields': ('rating', 'review_count')}),
        ('Flags', {'fields': ('is_featured', 'is_trending', 'is_flash_sale', 'is_active')}),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['short_id', 'user', 'status', 'payment_method', 'total', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__username', 'full_name', 'email']
    list_editable = ['status']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    def short_id(self, obj):
        return obj.short_id
    short_id.short_description = 'Order ID'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'max_uses', 'used_count', 'is_active', 'expiry_date']
    list_editable = ['is_active', 'discount_percent']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'total_items', 'created_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(NewsletterSubscription)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_editable = ['is_read']


# Customize Admin Site
admin.site.site_header = "LuxeShop Admin"
admin.site.site_title = "LuxeShop Administration"
admin.site.index_title = "Welcome to LuxeShop Admin Panel"
