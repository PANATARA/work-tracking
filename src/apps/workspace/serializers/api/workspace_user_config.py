from rest_framework import serializers

from core.constants import get_entity_model_and_serializer
from apps.projects.serializers.modules import ModuleShortReadOnlySerializer
from apps.users.serializers.internal.users import UserShortSerializer
from apps.workspace.models import workspace_user_config as wpuc
from apps.workspace.serializers.api.workspace import WorkspaceShortSerializer
from apps.workspace.serializers.api.workspace_config import TaskStatesSerializer, TaskStatesSerializerLite


class DisplayFiltersSerializer(serializers.ModelSerializer):
    assignee = UserShortSerializer(many=True)
    state = TaskStatesSerializerLite(many=True)
    module = ModuleShortReadOnlySerializer(many=True)
    created_by = UserShortSerializer(many=True)

    class Meta:
        model = wpuc.DisplayFilters
        fields = [
            "priority",
            "state", 
            "assignee", 
            "module", 
            "created_by"
        ]


class DisplayPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = wpuc.DisplayProperties
        fields = [
            "deadline",
            "priority",
            "assignees",
            "state",
            "module",
            "state_date",
            "tags",
        ]


class UserWorkspaceConfigSerializer(serializers.ModelSerializer):
    filters = DisplayFiltersSerializer(required=False)
    properties = DisplayPropertiesSerializer(required=False)
    user = UserShortSerializer(read_only=True)
    workspace = WorkspaceShortSerializer(read_only=True)

    class Meta:
        model = wpuc.UserWorkspaceConfig
        fields = [
            "user",
            "workspace",
            "layout",
            "order_by",
            "group_by",
            "show_empty_groups",
            "filters",
            "properties",
        ]

    def update(self, instance, validated_data):
        filters, properties = validated_data.pop("filters", False), validated_data.pop(
            "properties", False
        )

        if filters:
            for key, value in filters.items():
                setattr(instance.filters, key, value)
            instance.filters.save()

        if properties:
            for key, value in properties.items():
                setattr(instance.properties, key, value)
            instance.properties.save()

        return super().update(instance, validated_data)


class UserFavoriteCreateSerializer(serializers.Serializer):
    is_folder = serializers.BooleanField()
    name = serializers.CharField()
    entity_type = serializers.CharField(required=False, allow_null=True)
    entity_identifier = serializers.IntegerField(required=False, allow_null=True)
    parent = serializers.IntegerField(required=False, allow_null=True)


class UserFavoriteUpdateSerializer(serializers.Serializer):
    name = serializers.CharField()
    parent = serializers.IntegerField()
    sequence = serializers.FloatField()


class UserFavoriteReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserShortSerializer()
    workspace = WorkspaceShortSerializer()
    is_folder = serializers.BooleanField()
    name = serializers.CharField()
    entity_type = serializers.CharField()
    entity_identifier = serializers.IntegerField()
    entity_object = serializers.SerializerMethodField()
    parent = serializers.IntegerField()
    sequence = serializers.FloatField()

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
