from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status

from apps.notification.filters import NotificationFilter
from apps.notification.models.notification import Notification
from apps.notification.schema import notification_schema, send_notification_schema
from apps.notification.serializers.notification import SendNotificationToUserSerializer, NotificationSerializer
from apps.notification.celery_tasks import send_notification
from apps.workspace.permissions import IsWorkspaceAdmin


@notification_schema
class NotificationView(ModelViewSet):
    """
    API for working with user notifications.

    """

    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    http_method_names = ["get", "delete"]

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filterset_class = NotificationFilter
    search_fields = [
        "message",
    ]
    ordering = "-created_at"

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(
            user=user,
        ).select_related(
            "user",
            "triggered_by",
            "workspace",
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.save(update_fields=["is_read"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@send_notification_schema
class SendNotificationView(ViewSet):
    """API for sending notifications to members of the same workspace"""

    permission_classes = [IsWorkspaceAdmin]
    serializer_class = SendNotificationToUserSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        send_notification.delay(
            triggered_by=request.user.id,
            workspace_id=int(self.kwargs.get("workspace_id")),
            **validated_data,
        )
        return Response({"detail": "The process of sending notifications has begun"}, status=status.HTTP_201_CREATED)
