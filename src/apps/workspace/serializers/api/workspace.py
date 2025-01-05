from rest_framework import serializers

from core.serializers.mixins import InfoSerializerMixin
from apps.users.serializers.internal.users import UserShortSerializer
from apps.workspace.serializers.api.workspace_members import MemberSerializer


class WorkspaceSerializer(InfoSerializerMixin):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = UserShortSerializer(read_only=True)
    total_members = serializers.IntegerField(read_only=True)
    total_active_tasks = serializers.IntegerField(read_only=True)
    total_archived_tasks = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(read_only=True)
    workspace_members = MemberSerializer(read_only=True, many=True)
    absolute_url = serializers.SerializerMethodField(read_only=True)

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class WorkspaceShortSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = UserShortSerializer(read_only=True)
    name = serializers.CharField()
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
