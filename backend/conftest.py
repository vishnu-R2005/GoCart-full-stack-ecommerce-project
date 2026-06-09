import sys
from unittest.mock import MagicMock

# Mock razorpay before Django URL imports (Python 3.14 pkg_resources compat)
sys.modules.setdefault('razorpay', MagicMock())

import pytest
from rest_framework.test import APIClient

from tests.factories import AdminUserFactory, CategoryFactory, ProductFactory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def admin_user(db):
    return AdminUserFactory()


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def category(db):
    return CategoryFactory()


@pytest.fixture
def product(db, category):
    return ProductFactory(category=category)
