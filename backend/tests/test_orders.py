import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import AddressFactory


@pytest.mark.django_db
class TestOrders:
    def _add_to_cart(self, client, product):
        client.post(reverse('cart-add'), {'product_id': product.id, 'quantity': 1})

    def test_place_order(self, auth_client, user, product):
        address = AddressFactory(user=user)
        self._add_to_cart(auth_client, product)
        url = reverse('order-place')
        response = auth_client.post(url, {'shipping_address_id': address.id})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True

    def test_order_history(self, auth_client, user, product):
        address = AddressFactory(user=user)
        self._add_to_cart(auth_client, product)
        auth_client.post(reverse('order-place'), {'shipping_address_id': address.id})
        response = auth_client.get(reverse('order-list'))
        assert response.status_code == status.HTTP_200_OK
