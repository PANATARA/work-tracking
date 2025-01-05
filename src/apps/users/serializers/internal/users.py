from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    user_avatar = serializers.ImageField(source="user_avatar.image", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "absolute_url",
            "user_avatar",
        )

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    

class UserRoleShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    absolute_url = serializers.SerializerMethodField()
    user_avatar = serializers.ImageField(source="user_avatar.image", read_only=True)
    role = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "absolute_url",
            "user_avatar",
            "role"
        )

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    