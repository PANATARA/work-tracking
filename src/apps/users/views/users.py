from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import get_object_or_404 as get_object_or_HTTP404

from core.models.image_keeper import ImageKeeper
from apps.users.models.users_settings import UserSettings
from apps.users.serializers import users as user_s
from apps.users.schema import (
    user_registration_schema,
    user_change_password_schema,
    user_me_profile_schema,
    user_me_settings_schema,
    user_me_upload_avatar_schema,
    users_search_schema,
)

User = get_user_model()


@user_registration_schema
class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # JWT token generation
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)


@user_change_password_schema
class ChangePasswordView(APIView):

    def post(self, request):
        user = request.user
        serializer = user_s.ChangePasswordSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


@user_me_profile_schema
class MeView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch']

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return user_s.MeUpdateSerializer
        return user_s.MeSerializer
    
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            id=user
        ).select_related(
            "settings",
            "profile",
            "user_avatar",
        )

    def get_object(self):
        return self.request.user


@user_me_settings_schema
class UserSettingsView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = user_s.UserSettingsSerializer
    http_method_names = ['get', 'patch', "put"]
    
    def get_object(self):
        
        return UserSettings.objects.get(user=self.request.user)


@user_me_upload_avatar_schema
class UserUploadAvatarApi(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = user_s.UserUploadAvatarSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        ImageKeeper.objects.filter(user=user).delete()

        ImageKeeper.objects.create(
            image=serializer.validated_data["image"],
            user=user,
            task=None
        )

        return Response({"message": "Avatar uploaded successfully"}, status=status.HTTP_201_CREATED)


@users_search_schema
class GetUserInformation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_HTTP404(
            User.objects.select_related("profile", "user_avatar").only('id', 'username'),
            id=user_id
        )
        serializer = user_s.UserSearchSerializer(user)
        return Response(serializer.data)
