import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAuthentication:
    def test_register(self, api_client):
        url = reverse('register')
        data = {
            'email': 'newuser@test.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True
        assert 'tokens' in response.data

    def test_login(self, api_client, user):
        url = reverse('login')
        response = api_client.post(url, {'email': user.email, 'password': 'TestPass123!'})
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data['tokens']

    def test_profile(self, auth_client, user):
        url = reverse('profile')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email


@pytest.mark.django_db
class TestAddresses:
    def test_create_address(self, auth_client):
        url = reverse('address-list')
        data = {
            'full_name': 'Test User',
            'phone': '+919876543210',
            'address_line1': '123 Main St',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400001',
            'country': 'India',
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
