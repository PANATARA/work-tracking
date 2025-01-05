from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework import status

from apps.users.serializers import users


user_registration_schema = extend_schema_view(

    post=extend_schema(
        summary='User registration in the system', 
        tags=['Authentication & Authorization']
    )
)


user_change_password_schema = extend_schema_view(

    post=extend_schema(
        summary='Change password', 
        request=users.ChangePasswordSerializer,
        tags=['Authentication & Authorization']),
)


user_me_profile_schema = extend_schema_view(

    get=extend_schema(
        tags=['Users -> Profile'],
        summary='User profile', 
    ),

    put=extend_schema(
        tags=['Users -> Profile'],
        summary='Edit user profile', 
    ),

    patch=extend_schema(
        tags=['Users -> Profile'],
        summary='Partially edit user profile', 
    ),
)


users_search_schema = extend_schema_view(

    get=extend_schema(summary='Get user information by id', tags=['Users -> Profile']),
)


user_me_settings_schema = extend_schema_view(

    get=extend_schema(
        tags=['Users -> Settings'],
        summary='Get user\'s settings', 
    ),

    put=extend_schema(
        tags=['Users -> Settings'],
        summary='Change user\'s settings', 
    ),

    patch=extend_schema(
        tags=['Users -> Settings'],
        summary='Partial change user\'s settings', 
    ),
)


user_me_upload_avatar_schema = extend_schema_view(
    post=extend_schema(
        tags=['Users -> Profile'],
        summary='Upload new user\'s avatar',
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Avatar uploaded successfully",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Validation error"
            )
        },
    )
)