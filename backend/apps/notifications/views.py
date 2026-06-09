from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @extend_schema(tags=['Notifications'])
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        unread = self.get_queryset().filter(is_read=False).count()
        return Response({'success': True, 'unread_count': unread, **response.data})

    @extend_schema(tags=['Notifications'])
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({'success': True})

    @extend_schema(tags=['Notifications'])
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'success': True, 'message': 'All notifications marked as read.'})
