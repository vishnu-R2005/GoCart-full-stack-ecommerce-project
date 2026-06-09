import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from apps.accounts.models import Address, User, UserRole
from apps.orders.models import Coupon, CouponType
from apps.products.models import Category, Product


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@test.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'TestPass123!')
    role = UserRole.CUSTOMER
    is_verified = True


class AdminUserFactory(UserFactory):
    email = factory.Sequence(lambda n: f'admin{n}@test.com')
    role = UserRole.ADMIN
    is_staff = True


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    user = factory.SubFactory(UserFactory)
    full_name = factory.Faker('name')
    phone = '+919876543210'
    address_line1 = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state')
    postal_code = '110001'
    country = 'India'


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')
    slug = factory.Sequence(lambda n: f'category-{n}')
    is_active = True


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    slug = factory.Sequence(lambda n: f'product-{n}')
    description = factory.Faker('paragraph')
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    stock = 100
    sku = factory.Sequence(lambda n: f'SKU-{n:06d}')
    brand = factory.Faker('company')
    category = factory.SubFactory(CategoryFactory)
    is_active = True


class CouponFactory(DjangoModelFactory):
    class Meta:
        model = Coupon

    code = factory.Sequence(lambda n: f'SAVE{n}')
    coupon_type = CouponType.PERCENTAGE
    value = 10
    min_order_amount = 0
    is_active = True
    valid_from = factory.LazyFunction(lambda: timezone.now() - timezone.timedelta(days=1))
    valid_until = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=30))
