import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAnalytics:
    def test_dashboard_admin_only(self, auth_client):
        url = reverse('analytics-dashboard')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_dashboard_admin(self, admin_client):
        url = reverse('analytics-dashboard')
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'stats' in response.data
