from rest_framework import serializers

from apps.users.serializers.users import UserShortSerializer


class TagSerializerMixin(serializers.Serializer):
    tags_names = serializers.SerializerMethodField()

    def get_tags_names(self, obj):
        return [tag.name for tag in obj.tags.all()]


class StateDisplaySerializerMixin(serializers.Serializer):
    state_display = serializers.SerializerMethodField()

    def get_state_display(self, obj):
        return obj.get_state_display()


class InfoSerializerMixin(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = UserShortSerializer(read_only=True)
    updated_by = UserShortSerializer(read_only=True)
