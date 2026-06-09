import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCart:
    def test_add_to_cart(self, auth_client, product):
        url = reverse('cart-add')
        response = auth_client.post(url, {'product_id': product.id, 'quantity': 2})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True

    def test_get_cart(self, auth_client, product):
        auth_client.post(reverse('cart-add'), {'product_id': product.id, 'quantity': 1})
        response = auth_client.get(reverse('cart-list'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['item_count'] == 1

    def test_remove_from_cart(self, auth_client, product):
        auth_client.post(reverse('cart-add'), {'product_id': product.id, 'quantity': 1})
        url = reverse('cart-remove', kwargs={'product_id': product.id})
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
