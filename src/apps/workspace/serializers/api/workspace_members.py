from rest_framework import serializers
from crum import get_current_user

from apps.users.serializers.internal.users import UserShortSerializer
from apps.workspace.models.workspace import WorkspaceMember


class MemberSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserShortSerializer(read_only=True)
    role = serializers.IntegerField()
    date_joined = serializers.DateField(read_only=True)

    def update(self, instance, validated_data):
        current_user = get_current_user()
        try:
            user = WorkspaceMember.objects.get(user=current_user, workspace=instance.workspace)
        except WorkspaceMember.DoesNotExist:
            raise serializers.ValidationError("Current user is not a member of this workspace.")

        if user.role > instance.role:
            instance.role = validated_data.get("role", instance.role)
            instance.save()
        else:
            raise serializers.ValidationError("You do not have permission to update this member's role.")

        return instance

            