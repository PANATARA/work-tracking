from rest_framework import serializers

from apps.projects.serializers.modules import ModuleShortReadOnlySerializer
from apps.projects.serializers.projects import ProjectShortReadOnlySerializer
from apps.projects.serializers.tags import TagSerializer
from core.serializers.mixins import InfoSerializerMixin, TagSerializerMixin
from apps.projects.models import tasks
from apps.users.serializers import users
from apps.workspace.serializers.workspace import WorkspaceShortSerializer
from apps.workspace.serializers.workspace_config import TaskStatesSerializer, TaskStatesSerializerLite


class TaskReadOnlySerializer(InfoSerializerMixin):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    assignees = users.UserRoleShortSerializer(many=True)
    tags = TagSerializer(many=True)
    state = TaskStatesSerializerLite()
    priority = serializers.IntegerField()
    deadline = serializers.DateTimeField()
    resolution_text = serializers.CharField()
    workspace = WorkspaceShortSerializer()
    project = ProjectShortReadOnlySerializer()
    module = ModuleShortReadOnlySerializer()
    is_subscriber = serializers.BooleanField()



class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required = True)
    description = serializers.CharField(required=False)
    priority = serializers.IntegerField(required=False)
    deadline = serializers.DateTimeField(required=False)
    state_id = serializers.IntegerField(required=False)
    module_id = serializers.IntegerField(required=False)
    assignees = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, required=False
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=30), allow_empty=True, write_only=True, required=False
    )


class TaskUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required = False)
    description = serializers.CharField(required=False)
    state_id = serializers.IntegerField(required=False)
    assignees = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, required=False
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=30), allow_empty=True, write_only=True, required=False
    )
    priority = serializers.IntegerField(required=False)
    deadline = serializers.DateTimeField(required=False)
    module_id = serializers.IntegerField(required=False)
    

    class Meta:
        model = tasks.Task
        fields = (
            "id",
            "title",
            "description",
            "state",
            "assignees",
            "tags",
            "priority",
            "deadline",
            "module",
            "resolution_text",
        )


class DashboardTaskSerializer(TagSerializerMixin,serializers.ModelSerializer):
    project = ProjectShortReadOnlySerializer()
    module = ModuleShortReadOnlySerializer()
    assignees = users.UserShortSerializer(many=True)
    state = TaskStatesSerializer()

    class Meta:
        model = tasks.Task
        fields = (
            "id",
            "title",
            "deadline",
            "priority",
            "assignees",
            "state",
            "module",
            "tags_names",
            "project",
        )


class TaskTransferSerializer(serializers.Serializer):
    task = serializers.ListField(
        child=serializers.IntegerField(
            min_value=0,
        ),
    )
    module = serializers.IntegerField(
        min_value=0,
    )


class TaskShortReadOnlySerializer(serializers.ModelSerializer):
    state = TaskStatesSerializer()
    task_absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = tasks.Task
        fields = (
            "id",
            "title",
            "state",
            "priority",
            "deadline",
            "workspace",
            "project",
            "task_absolute_url",
        )

    def get_task_absolute_url(self, obj):
        return obj.get_absolute_url()