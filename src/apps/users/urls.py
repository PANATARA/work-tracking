from django.urls import path

from apps.users.views import users

urlpatterns = [
    path(
        "users/search/<int:user_id>/",
        users.GetUserInformation.as_view(),
        name="users-profile",
    ),
    path(
        "users/reg/", 
        users.RegistrationView.as_view(), 
        name="reg"
    ),
    path(
        "users/me/", 
        users.MeView.as_view(), 
        name="me"
    ),
    path(
        "users/change-passwd/", 
        users.ChangePasswordView.as_view(), 
        name="change_passwd"
    ),
    path(
        "users/settings", 
        users.UserSettingsView.as_view(), 
        name="user-settings"
    ),
    path(
        "users/upload-avatar",
        users.UserUploadAvatarApi.as_view(),
        name="user-upload-avatar",
    ),
]
