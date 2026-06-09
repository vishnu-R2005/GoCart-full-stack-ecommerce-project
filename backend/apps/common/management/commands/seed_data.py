from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from apps.accounts.models import User, UserRole
from apps.orders.models import Coupon, CouponType
from apps.products.models import Category, Product


class Command(BaseCommand):
    help = 'Seed GoCart with sample categories, products, admin user, and coupons'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            email='admin@gocart.com',
            defaults={
                'first_name': 'GoCart',
                'last_name': 'Admin',
                'role': UserRole.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True,
            },
        )
        if created:
            admin.set_password('Admin@123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin: admin@gocart.com / Admin@123'))

        categories_data = [
            ('Electronics', ['Smartphones', 'Laptops', 'Headphones']),
            ('Fashion', ['Men', 'Women', 'Kids']),
            ('Home', ['Furniture', 'Kitchen', 'Decor']),
        ]

        for cat_name, children in categories_data:
            parent, _ = Category.objects.get_or_create(
                slug=slugify(cat_name),
                defaults={'name': cat_name, 'description': f'{cat_name} products'},
            )
            for child_name in children:
                Category.objects.get_or_create(
                    slug=slugify(f'{cat_name}-{child_name}'),
                    defaults={'name': child_name, 'parent': parent},
                )

        all_cats = list(Category.objects.filter(parent__isnull=False))
        brands = ['Samsung', 'Apple', 'Sony', 'Nike', 'Adidas', 'IKEA']
        for i in range(1, 25):
            cat = all_cats[i % len(all_cats)]
            sku = f'GC-{i:05d}'
            Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': f'GoCart Product {i}',
                    'slug': f'gocart-product-{i}',
                    'description': f'High quality product {i} from GoCart. Shop Smarter. Shop Faster.',
                    'price': Decimal('999.00') + i * 100,
                    'discount_price': Decimal('899.00') + i * 80 if i % 3 == 0 else None,
                    'stock': 50 + i,
                    'brand': brands[i % len(brands)],
                    'category': cat,
                    'is_featured': i <= 8,
                    'is_active': True,
                },
            )

        now = timezone.now()
        Coupon.objects.get_or_create(
            code='WELCOME10',
            defaults={
                'description': '10% off welcome coupon',
                'coupon_type': CouponType.PERCENTAGE,
                'value': Decimal('10'),
                'min_order_amount': Decimal('500'),
                'max_discount': Decimal('1000'),
                'valid_from': now - timezone.timedelta(days=1),
                'valid_until': now + timezone.timedelta(days=365),
            },
        )
        Coupon.objects.get_or_create(
            code='FLAT200',
            defaults={
                'description': '₹200 flat discount',
                'coupon_type': CouponType.FIXED,
                'value': Decimal('200'),
                'min_order_amount': Decimal('1000'),
                'valid_from': now - timezone.timedelta(days=1),
                'valid_until': now + timezone.timedelta(days=365),
            },
        )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))
