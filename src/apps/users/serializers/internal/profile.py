from rest_framework import serializers

from apps.users.models.profile import Profile


class ProfileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "bio",
            "telegram_id",
            "github",
            "linkedin",
            "company",
            "position",
            "location",
        )
