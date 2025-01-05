from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.constants import get_entity_model_and_serializer
from apps.notification.models.notification import Notification
from apps.users.serializers.internal.users import UserShortSerializer

User = get_user_model()


class SendNotificationToUserSerializer(serializers.Serializer):
    users_ids = serializers.ListField(child=serializers.IntegerField())
    message = serializers.CharField()
    notification_type = serializers.IntegerField()
    entity_type = serializers.CharField()
    entity_identifier = serializers.IntegerField()


class NotificationSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    triggered_by = UserShortSerializer()
    entity_object = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "triggered_by",
            "entity_type",
            "entity_identifier",
            "entity_object",
            "type",
            "is_read",
            "message",
            "created_at",
        ]
    
    def get_entity_object(self, obj):
        entity_type = obj.entity_type
        entity_identifier = obj.entity_identifier

        entity_model, entity_serializer = get_entity_model_and_serializer(
            entity_type
        )
        if entity_model and entity_serializer:
            try:
                entity = entity_model.objects.get(pk=entity_identifier)
                return entity_serializer(entity).data
            except entity_model.DoesNotExist:
                return None
        return None
