from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.timezone import now

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        self.user.last_login = now()
        self.user.save(update_fields=["last_login"])
        return data
