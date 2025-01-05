from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.projects.models import modules
from core.serializers.mixins import InfoSerializerMixin
from apps.projects.serializers.projects import ProjectShortReadOnlySerializer
from apps.projects.validators import validate_start_end_dates
from apps.workspace.serializers.workspace import WorkspaceShortSerializer

User = get_user_model()

class ModuleReadOnlySerializer(InfoSerializerMixin):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    goal = serializers.CharField(read_only=True)
    date_start = serializers.DateTimeField(read_only=True)
    date_end = serializers.DateTimeField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    project = ProjectShortReadOnlySerializer(read_only=True)
    workspace = WorkspaceShortSerializer(read_only=True)

    tasks_count = serializers.IntegerField(read_only=True)
    completed_tasks_count = serializers.IntegerField(read_only=True)
    absolute_url = serializers.SerializerMethodField(read_only=True)


    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class ModuleUpdateCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    goal = serializers.CharField(required=False)
    date_start = serializers.DateTimeField(required=False)
    date_end = serializers.DateTimeField(required=False)
    status = serializers.IntegerField(required=False)


    class Meta:
        model = modules.Module
        fields = (
            "id",
            "name",
            "description",
            "goal",
            "date_start",
            "date_end",
            "status",
        )

    def validate(self, attrs):
        attrs["date_start"], attrs["date_end"] = validate_start_end_dates(
            attrs.get("date_start"), attrs.get("date_end")
        )

        return attrs
    
    def create(self, validated_data):
        project_id = self.context["project_id"]
        workspace_id = self.context["workspace_id"]
        validated_data["project_id"] = project_id
        validated_data["workspace_id"] = workspace_id
        return super().create(validated_data)


class ModuleShortReadOnlySerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = modules.Module
        fields = (
            "id",
            "name",
            "status",
            "absolute_url",
        )

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    
    def get_status(self, obj):
        return obj.get_status_display()
