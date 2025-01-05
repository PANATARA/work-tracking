from rest_framework import serializers

from apps.workspace.models.workspace_config import (
    TaskState,
    ProjectState,
)


class WorkspaceConfigurationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    workspace = serializers.PrimaryKeyRelatedField(read_only=True)
    archive_completed_task = serializers.BooleanField(required=False)
    archive_after = serializers.DurationField(required=False)

    class Meta:
        model = ProjectState
        fields = (
            "id",
            "workspace",
            "archive_completed_task",
            "archive_after",
        )


class ProjectStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectState
        fields = "__all__"


class TaskStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = "__all__"


class TaskStatesSerializerLite(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    type = serializers.IntegerField(read_only=True)

