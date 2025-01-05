from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers.mixins import InfoSerializerMixin
from apps.users.serializers.users import UserShortSerializer
from apps.workspace.serializers.workspace import WorkspaceShortSerializer
from apps.workspace.serializers.workspace_config import ProjectStatesSerializer

User = get_user_model()


class ProjectReadOnlySerializer(InfoSerializerMixin):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    manager = UserShortSerializer()
    state = ProjectStatesSerializer()
    workspace = WorkspaceShortSerializer()
    date_start = serializers.DateTimeField(required=False)
    date_end = serializers.DateTimeField(required=False)

    user_is_author = serializers.BooleanField(read_only=True)
    user_is_manager = serializers.BooleanField(read_only=True)
    total_active_tasks = serializers.IntegerField(read_only=True)
    total_archived_tasks = serializers.IntegerField(read_only=True)
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class ProjectCreateUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    manager = serializers.IntegerField(required=False)
    state = serializers.IntegerField(required=False)
    date_start = serializers.DateTimeField(required=False)
    date_end = serializers.DateTimeField(required=False)


class ProjectShortReadOnlySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    state = ProjectStatesSerializer()
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
