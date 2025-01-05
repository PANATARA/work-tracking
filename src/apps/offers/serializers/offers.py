from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError
from rest_framework import serializers

from core.serializers.mixins import StateDisplaySerializerMixin
from apps.offers.services.offer_service import OfferService as of
from apps.users.serializers.users import UserShortSerializer
from apps.workspace.models.workspace import Workspace
from apps.offers.models.offers import Offer

User = get_user_model()

"""
Serializers from the workspace side
"""


class AdminOfferListSerializer(StateDisplaySerializerMixin,serializers.ModelSerializer):
    user = UserShortSerializer()
    created_by = UserShortSerializer()
    updated_by = UserShortSerializer()
    state_display = serializers.CharField()

    class Meta:
        model = Offer
        fields = (
            "id",
            "user",
            "state_display",
            "message_text",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        )


class AdminOfferCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = (
            "id",
            "user",
            "message_text",
            "user_role"
        )

    def __init__(self, *args, **kwargs):
        self.workspace_id = kwargs["context"].get("workspace_id")
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        try:
            workspace = Workspace.objects.get(id=self.workspace_id)
        except Workspace.DoesNotExist:
            raise serializers.ValidationError("Workspace not found")
        attrs["workspace"] = workspace
        attrs["message_text"] = of.generate_message(attrs["user_role"], attrs["message_text"])

        return attrs


class AdminOfferUpdateSerializer(serializers.ModelSerializer):
    accept = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Offer
        fields = (
            "id",
            "message_text",
            "accept",
        )

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if "accept" in data:
            data["workspace_accept"] = data.pop("accept")
        return data

    def validate(self, attrs):
        if self.instance.user_accept is not None:
            raise ParseError("The offer is closed. Changes are not available.")
        else:
            if not self.instance.workspace_accept:
                raise ParseError("The offer is closed. Changes are not available.")
        return attrs


"""
Serializers from the user side
"""


class UserOfferListSerializer(serializers.ModelSerializer):
    # workspace = workspace.WorkspaceShortSerializer()
    status = serializers.CharField()

    class Meta:
        model = Offer
        fields = (
            "id",
            "workspace",
            "status",
            "message_text",
            "user_accept",
            "is_read_by_user",
        )


class UserOfferUpdateSerializer(serializers.ModelSerializer):
    accept = serializers.BooleanField(write_only=True)

    class Meta:
        model = Offer
        fields = (
            "id",
            "accept",
        )

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["user_accept"] = data.pop("accept")
        return data

    def validate(self, attrs):
        if self.instance.user_accept is not None:
            raise ParseError("Offer is closed. Change not available.")
        else:
            if not self.instance.admin_accept:
                raise ParseError("Offer is closed. Change not available.")
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if instance.user_accept and instance.admin_accept:
                of.add_user_to_workspace_by_offer(instance)    
        return instance
