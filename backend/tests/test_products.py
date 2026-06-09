import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProducts:
    def test_list_products(self, api_client, product):
        url = reverse('product-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_product_detail(self, api_client, product):
        url = reverse('product-detail', kwargs={'slug': product.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == product.name

    def test_featured_products(self, api_client, product):
        product.is_featured = True
        product.save()
        url = reverse('product-featured')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1


@pytest.mark.django_db
class TestCategories:
    def test_category_tree(self, api_client, category):
        url = reverse('category-list') + '?tree=true'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
