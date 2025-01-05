from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from django.db import transaction

from apps.users.models.users_settings import UserSettings
from apps.users.serializers.profile import ProfileShortSerializer

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
        )

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError("Email duplicate")
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("old_password", "new_password")

    def validate(self, attrs):
        user = self.instance
        old_password = attrs.pop("old_password")
        if not user.check_password(old_password):
            raise ParseError("Check that password is correct")
        return attrs

    def validate_password_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("new_password")
        instance.set_password(password)
        instance.save()
        return instance


class UserSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSettings
        fields = (
            "id",
            "last_workspace_id",
            "app_theme",
            "language",
            "auto_subsсribe_to_task",
            "mention",
        )


class UserUploadAvatarSerializer(serializers.Serializer):
    image = serializers.ImageField()


class MeSerializer(serializers.ModelSerializer):
    profile = ProfileShortSerializer()
    settings = UserSettingsSerializer()
    user_avatar = serializers.ImageField(source="user_avatar.image", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "user_avatar",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "date_joined",
            "profile",
            "settings",
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileShortSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "username",
            "profile",
        )

    def update(self, instance, validated_data):
        profile_data = (
            validated_data.pop("profile") if "profile" in validated_data else None
        )

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if profile_data:
                self._update_profile(profile=instance.profile, data=profile_data)

        return instance

    def _update_profile(self, profile, data):
        profile_serializer = ProfileShortSerializer(
            instance=profile, data=data, partial=True
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()


class UserSearchSerializer(serializers.ModelSerializer):
    user_avatar = serializers.ImageField(source="user_avatar.image", read_only=True)
    profile = ProfileShortSerializer()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "user_avatar",
            "full_name",
            "profile",
        )
    
    def get_full_name(self, obj):     
        return "Full Name"


class UserShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    absolute_url = serializers.SerializerMethodField()
    user_avatar = serializers.ImageField(source="user_avatar.image", read_only=True)

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    

class UserRoleShortSerializer(UserShortSerializer):
    role = serializers.IntegerField()