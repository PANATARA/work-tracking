from rest_framework import serializers

from apps.activitylog import models
from apps.users.serializers.internal.users import UserShortSerializer


class ListTaskLogsSerializer(serializers.ModelSerializer):
    action_type_display = serializers.SerializerMethodField()
    user = UserShortSerializer()

    class Meta:
        model = models.TaskActivityLog
        fields = (
            "id",
            "task",
            "user",
            "action_type_display",
            "field",
            "value",
            "detail",
            "timestamp",
        )

    def get_action_type_display(self, obj):
        return obj.get_action_type_display()
