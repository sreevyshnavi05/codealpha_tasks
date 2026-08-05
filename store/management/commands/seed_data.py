from django.core.management.base import BaseCommand
from store.models import Category, Product, ProductImage, Coupon, Review
from django.contrib.auth.models import User
import random


CATEGORIES = [
    {'name': 'Electronics', 'icon': 'fas fa-laptop', 'description': 'Latest gadgets and electronics'},
    {'name': 'Fashion', 'icon': 'fas fa-tshirt', 'description': 'Trendy clothing and apparel'},
    {'name': 'Shoes', 'icon': 'fas fa-shoe-prints', 'description': 'Stylish footwear for all occasions'},
    {'name': 'Watches', 'icon': 'fas fa-clock', 'description': 'Premium timepieces and smartwatches'},
    {'name': 'Home Decor', 'icon': 'fas fa-couch', 'description': 'Beautiful home accessories'},
    {'name': 'Beauty', 'icon': 'fas fa-spa', 'description': 'Skincare, makeup and beauty products'},
    {'name': 'Books', 'icon': 'fas fa-book', 'description': 'Best sellers and educational books'},
]

PRODUCTS = [
    # Electronics
    {'name': 'MacBook Pro 16"', 'category': 'Electronics', 'brand': 'Apple', 'price': 249999, 'discount_price': 219999,
     'description': 'The most powerful MacBook Pro ever. With M3 Max chip, stunning Liquid Retina XDR display, and up to 22 hours battery life.',
     'features': 'M3 Max chip|Liquid Retina XDR Display|Up to 128GB Unified Memory|Up to 8TB SSD Storage|MagSafe charging|22-hour battery life',
     'specifications': 'Processor: Apple M3 Max|RAM: 32GB|Storage: 1TB SSD|Display: 16.2-inch|Weight: 2.14kg',
     'stock': 15, 'rating': 4.9, 'is_featured': True, 'is_trending': True,
     'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&q=80'},

    {'name': 'iPhone 15 Pro Max', 'category': 'Electronics', 'brand': 'Apple', 'price': 134900, 'discount_price': 124900,
     'description': 'Titanium. So strong. So light. So Pro. The ultimate iPhone with A17 Pro chip and the most advanced camera system.',
     'features': 'A17 Pro chip|48MP Pro camera system|USB-C|Action Button|5G connectivity|ProMotion display',
     'specifications': 'Chip: A17 Pro|RAM: 8GB|Storage: 256GB|Display: 6.7-inch Super Retina XDR|Battery: 4422mAh',
     'stock': 25, 'rating': 4.8, 'is_featured': True, 'is_flash_sale': True,
     'image': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&q=80'},

    {'name': 'Sony WH-1000XM5', 'category': 'Electronics', 'brand': 'Sony', 'price': 29990, 'discount_price': 22990,
     'description': 'Industry-leading noise cancellation headphones with 30-hour battery life and crystal-clear hands-free calling.',
     'features': 'Industry-leading ANC|30-hour battery|Multipoint connection|Speak-to-chat|360 Reality Audio',
     'specifications': 'Driver: 30mm|Frequency: 4Hz–40,000Hz|Weight: 250g|Charging: USB-C|Codec: LDAC',
     'stock': 40, 'rating': 4.7, 'is_trending': True, 'is_flash_sale': True,
     'image': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=600&q=80'},

    {'name': 'iPad Pro 12.9"', 'category': 'Electronics', 'brand': 'Apple', 'price': 112900, 'discount_price': 99900,
     'description': 'Your next computer is not a computer. Supercharged by M2 chip with Ultra Retina XDR display.',
     'features': 'M2 chip|Ultra Retina XDR display|Apple Pencil (2nd gen) support|Center Stage|5G capable',
     'specifications': 'Chip: M2|Display: 12.9-inch Liquid Retina XDR|Storage: 256GB|Camera: 12MP Wide',
     'stock': 20, 'rating': 4.8, 'is_featured': True,
     'image': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&q=80'},

    {'name': 'Samsung 65" QLED 4K TV', 'category': 'Electronics', 'brand': 'Samsung', 'price': 89999, 'discount_price': 69999,
     'description': 'Experience breathtaking 4K QLED picture quality with AI-powered upscaling and Smart TV features.',
     'features': 'Quantum Dot technology|4K AI Upscaling|Object Tracking Sound|Smart TV platform|120Hz refresh',
     'specifications': 'Screen Size: 65"|Resolution: 4K UHD|HDR: Quantum HDR|Refresh Rate: 120Hz|HDMI: 4 ports',
     'stock': 10, 'rating': 4.6, 'is_featured': True,
     'image': 'https://images.unsplash.com/photo-1593784991095-a205069470b6?w=600&q=80'},

    # Fashion
    {'name': 'Premium Leather Jacket', 'category': 'Fashion', 'brand': 'LuxeStyle', 'price': 12999, 'discount_price': 8999,
     'description': 'Genuine Italian leather jacket with a slim fit silhouette. Timeless design that elevates any outfit.',
     'features': 'Genuine Italian leather|YKK zippers|Quilted lining|Multiple pockets|Slim fit design',
     'specifications': 'Material: 100% Genuine Leather|Lining: Polyester|Closure: Zipper|Fit: Slim',
     'stock': 30, 'rating': 4.5, 'is_trending': True,
     'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&q=80'},

    {'name': 'Designer Silk Dress', 'category': 'Fashion', 'brand': 'Elegance', 'price': 8999, 'discount_price': 5999,
     'description': 'Luxurious silk midi dress with a flattering wrap silhouette. Perfect for both day and evening occasions.',
     'features': '100% Pure silk|Wrap-around design|Adjustable waistband|Midi length|Hand wash recommended',
     'specifications': 'Material: 100% Silk|Length: Midi|Fit: Wrap|Care: Dry clean only',
     'stock': 25, 'rating': 4.6, 'is_featured': True, 'is_flash_sale': True,
     'image': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600&q=80'},

    {'name': 'Classic Denim Jeans', 'category': 'Fashion', 'brand': 'DenimCo', 'price': 3999, 'discount_price': 2499,
     'description': 'Premium stretch denim jeans with a perfect slim fit. The wardrobe essential that never goes out of style.',
     'features': 'Stretch denim fabric|Slim fit cut|5-pocket design|Machine washable|Fade-resistant color',
     'specifications': 'Material: 98% Cotton 2% Elastane|Fit: Slim|Rise: Mid-rise|Wash: Machine wash cold',
     'stock': 60, 'rating': 4.4, 'is_trending': True,
     'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&q=80'},

    # Shoes
    {'name': 'Nike Air Jordan 1', 'category': 'Shoes', 'brand': 'Nike', 'price': 12995, 'discount_price': 10995,
     'description': 'The iconic Air Jordan 1 sneaker in premium leather. A cultural icon that transcends basketball.',
     'features': 'Full-grain leather upper|Air-Sole unit|Rubber outsole|Padded collar|Iconic Wings logo',
     'specifications': 'Upper: Leather|Sole: Rubber|Closure: Lace-up|Available sizes: 6-13',
     'stock': 35, 'rating': 4.9, 'is_featured': True, 'is_trending': True,
     'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80'},

    {'name': 'Adidas Ultraboost 23', 'category': 'Shoes', 'brand': 'Adidas', 'price': 17999, 'discount_price': 13999,
     'description': 'Experience incredible energy return with Boost cushioning technology. The ultimate running shoe.',
     'features': 'Boost midsole|Primeknit+ upper|Continental rubber outsole|Torsion system|Lightstrike EVA',
     'specifications': 'Upper: Primeknit+|Sole: Continental rubber|Drop: 10mm|Weight: 310g',
     'stock': 28, 'rating': 4.7, 'is_flash_sale': True,
     'image': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=600&q=80'},

    # Watches
    {'name': 'Apple Watch Ultra 2', 'category': 'Watches', 'brand': 'Apple', 'price': 89900, 'discount_price': 79900,
     'description': 'The most rugged and capable Apple Watch. Built for endurance athletes and outdoor adventurers.',
     'features': 'Always-On Retina display|Up to 60-hour battery|Precision dual-frequency GPS|Action Button|Water resistant 100m',
     'specifications': 'Case: Titanium|Display: 49mm|Battery: Up to 60 hours|Water resistance: 100m|Chip: S9',
     'stock': 12, 'rating': 4.8, 'is_featured': True,
     'image': 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&q=80'},

    {'name': 'Rolex Submariner', 'category': 'Watches', 'brand': 'Rolex', 'price': 999900, 'discount_price': None,
     'description': 'The reference among divers\' watches since 1953. Elegant, professional, and waterproof to 300 metres.',
     'features': 'Oyster case|Unidirectional rotatable bezel|300m water resistance|Automatic movement|Scratch-resistant sapphire crystal',
     'specifications': 'Case: Oystersteel|Movement: Automatic|Water resistance: 300m|Case diameter: 41mm',
     'stock': 3, 'rating': 5.0, 'is_trending': True,
     'image': 'https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=600&q=80'},

    # Home Decor
    {'name': 'Luxury Scented Candle Set', 'category': 'Home Decor', 'brand': 'AromaLux', 'price': 2999, 'discount_price': 1999,
     'description': 'A collection of 3 premium soy wax candles in elegant glass vessels. Fill your home with luxury fragrances.',
     'features': '100% soy wax|Lead-free cotton wick|50-hour burn time|Premium fragrance oils|Reusable glass vessel',
     'specifications': 'Material: Soy wax|Burn time: 50 hours each|Weight: 250g each|Scents: Lavender, Vanilla, Sandalwood',
     'stock': 50, 'rating': 4.6, 'is_featured': True, 'is_flash_sale': True,
     'image': 'https://images.unsplash.com/photo-1602523961358-f9f03dd557db?w=600&q=80'},

    # Beauty
    {'name': 'La Mer Moisturizing Cream', 'category': 'Beauty', 'brand': 'La Mer', 'price': 19999, 'discount_price': 16999,
     'description': 'The legendary moisturizer that started a skincare revolution. Transforms skin with healing Miracle Broth.',
     'features': 'Miracle Broth formula|Deep hydration|Cell renewal|Anti-aging properties|Suitable for all skin types',
     'specifications': 'Size: 60ml|Skin type: All|Key ingredient: Miracle Broth|Usage: Twice daily',
     'stock': 20, 'rating': 4.7, 'is_trending': True,
     'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&q=80'},

    # Books
    {'name': 'Atomic Habits', 'category': 'Books', 'brand': 'Penguin', 'price': 799, 'discount_price': 499,
     'description': 'The #1 New York Times bestseller. Transform your life with tiny changes and remarkable results.',
     'features': 'Practical strategies|Case studies|Science-backed|Habit tracking template|176k+ reviews',
     'specifications': 'Author: James Clear|Pages: 320|Language: English|Publisher: Avery|ISBN: 978-0735211292',
     'stock': 100, 'rating': 4.9, 'is_featured': True, 'is_trending': True,
     'image': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&q=80'},
]

COUPONS = [
    {'code': 'WELCOME10', 'discount_percent': 10, 'max_uses': 1000},
    {'code': 'LUXE20', 'discount_percent': 20, 'max_uses': 500},
    {'code': 'FLASH30', 'discount_percent': 30, 'max_uses': 100},
    {'code': 'SAVE15', 'discount_percent': 15, 'max_uses': 250},
]


class Command(BaseCommand):
    help = 'Seed database with sample categories, products, coupons'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Seeding database...'))

        # Create categories
        cat_objs = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon'], 'description': cat_data['description']}
            )
            cat_objs[cat.name] = cat
            if created:
                self.stdout.write(f'  [+] Category: {cat.name}')

        # Create products
        for p_data in PRODUCTS:
            cat = cat_objs.get(p_data['category'])
            if not cat:
                continue
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'category': cat,
                    'brand': p_data.get('brand', ''),
                    'price': p_data['price'],
                    'discount_price': p_data.get('discount_price'),
                    'description': p_data.get('description', ''),
                    'features': p_data.get('features', ''),
                    'specifications': p_data.get('specifications', ''),
                    'stock': p_data.get('stock', 20),
                    'rating': p_data.get('rating', 4.5),
                    'review_count': random.randint(10, 200),
                    'is_featured': p_data.get('is_featured', False),
                    'is_trending': p_data.get('is_trending', False),
                    'is_flash_sale': p_data.get('is_flash_sale', False),
                    'image': p_data.get('image', ''),
                }
            )
            if created:
                for i in range(3):
                    ProductImage.objects.create(
                        product=product,
                        image=p_data.get('image', ''),
                        alt_text=f"{product.name} - Image {i+1}"
                    )
                self.stdout.write(f'  [+] Product: {product.name}')

        # Create coupons
        for c_data in COUPONS:
            coupon, created = Coupon.objects.get_or_create(
                code=c_data['code'],
                defaults={'discount_percent': c_data['discount_percent'], 'max_uses': c_data['max_uses']}
            )
            if created:
                self.stdout.write(f'  [+] Coupon: {coupon.code}')

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('Available coupons: WELCOME10, LUXE20, FLASH30, SAVE15'))
