import django_filters

from apps.notification.models import notification


class NotificationFilter(django_filters.FilterSet):

    class Meta:
        model = notification.Notification
        fields = (
            "workspace",
            "type",
            "is_read",
        )