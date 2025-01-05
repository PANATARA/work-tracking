from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.workspace.serializers.api.workspace_user_config import (
    UserFavoriteCreateSerializer, 
    UserFavoriteReadSerializer, 
    UserFavoriteUpdateSerializer,
)

workspace = extend_schema_view(

    list=extend_schema(
        tags=["Workspace"],
        summary="Retrieve User's Workspaces",
        description="Fetch a list of all workspaces belonging to the current user. This endpoint returns details for each workspace that the user has access to.",
    ),

    retrieve=extend_schema(
        tags=["Workspace"],
        summary="Retrieve Workspace Details",
        description="Fetch detailed information about a specific workspace that the user has access to. This endpoint returns information on the workspace's properties, members, and permissions relevant to the current user.",
    ),

    create=extend_schema(
        tags=["Workspace"],
        summary="Creates a workspace and performs its basic setup",
        description=
"""
**Required Field**:
- name (string): The name of the new workspace.

**Functionality**:
This method performs the following actions:

- Create a Workspace: Initializes a new workspace with the provided name.
- Assign Ownership: Adds the user as a participant in the workspace with the role of "Owner."
- Set Up Project States: Generates default project states for the workspace.
- Set Up Task States: Creates default task states for task management within the workspace.
- Initialize Configuration: Establishes default settings for the workspace using a configuration model.

This ensures that the workspace is fully set up and ready for use.
""",
    ),

    partial_update=extend_schema(
        tags=["Workspace"],
        summary="Partially Update Workspace",
        description="Update specific fields of an existing workspace. This method allows you to change certain attributes without affecting the others.",
    ),

    update=extend_schema(
        tags=["Workspace"],
        summary="Update Workspace",
        description="Completely replace an existing workspace with new values. Ensure that you supply all required data to perform this operation.",
    ),

    destroy=extend_schema(
        tags=["Workspace"],
        summary="Delete Workspace",
        description="Remove the specified workspace permanently. This action deletes all associated data and cannot be undone.",
    ),
)


workspace_config = extend_schema_view(

    get=extend_schema(
        tags=["Workspace -> Configuration"],
        summary="Get workspace configuration", 
    ),

    patch=extend_schema(
        tags=["Workspace -> Configuration"],
        summary="Change workspace configuration",
    )
)


workspace_project_config = extend_schema_view(

    retrieve=extend_schema(
        tags=["Workspace -> Configuration -> Projects"],
        summary="Get project state", 
    ),

    list=extend_schema(
        tags=["Workspace -> Configuration -> Projects"],
        summary="Get project states", 
    ),

    create=extend_schema(
        tags=["Workspace -> Configuration -> Projects"],
        summary="Create project state", 
    ),

    destroy=extend_schema(
        tags=["Workspace -> Configuration -> Projects"],
        summary="Delete project state", 
    ),
)


workspace_project_config_reset_states = extend_schema(
    tags=["Workspace -> Configuration -> Projects"],
    summary="Reset projects states to default values", 
)


workspace_task_config = extend_schema_view(

    retrieve=extend_schema(
        tags=["Workspace -> Configuration -> Tasks"],
        summary="Get task state", 
    ),

    list=extend_schema(
        tags=["Workspace -> Configuration -> Tasks"],
        summary="Get task states", 
    ),

    create=extend_schema(
        tags=["Workspace -> Configuration -> Tasks"],
        summary="Create task state", 
    ),

    destroy=extend_schema(
        tags=["Workspace -> Configuration -> Tasks"],
        summary="Delete task state", 
    ),
)


workspace_task_config_reset_states = extend_schema(
    tags=["Workspace -> Configuration -> Tasks"],
    summary="Reset tasks states to default values",
)


member_schema = extend_schema_view(

    list=extend_schema(
        tags=["Workspace -> Member"],
        summary="List of workspace members", 
    ),

    retrieve=extend_schema(
        tags=["Workspace -> Member"],
        summary="Details about a member", 
    ),

    destroy=extend_schema(
        tags=["Workspace -> Member"],
        summary="Remove a member", 
        description=
"""
#### Role Choices:
- OWNER = 5
- ADMIN = 4
- MANAGER = 3
- MEMBER = 2
- OBSERVER = 1
"""
    ),

    partial_update=extend_schema(
        tags=["Workspace -> Member"],
        summary="Partially update a member",
        description=
"""
#### Role Choices:
- OWNER = 5
- ADMIN = 4
- MANAGER = 3
- MEMBER = 2
- OBSERVER = 1
""",
    ),
)


workspace_logout_schema = extend_schema(
    tags=["Workspace -> Member"],
    summary="Logout me from apps.workspace", 
    responses={204: "No Content"}
    # request=tasks.TaskTransferSerializer,  # указать сериализатор для входящих данных
)


reassign_workspace_owner_schema = extend_schema_view(

    post=extend_schema(
        tags=["Workspace -> Member"],
        summary="Assigns a different workspace owner",
    ),
)


user_workspace_config = extend_schema_view(

    retrieve=extend_schema(
        tags=["Workspace -> Configuration (Personal)"],
        summary="Get user workspace config", 
    ),

    partial_update=extend_schema(
        tags=["Workspace -> Configuration (Personal)"],
        summary="Partially change the configuration of the user's workspace",
        description=
"""
#### Layout Choices:
- LIST
- BOARD
- CALENDAR
- TABLE
- TIMELINE

#### Order Choices:
- UPDATED_AT
- CREATED_AT
- START_DATE
- DEADLINE
- PRIORITY

#### Group Choices:
- STATE
- PRIORITY
- MODULE
- TAG
- ASSIGNEE
- CREATED_BY
"""
    ),

    update=extend_schema(
        tags=["Workspace -> Configuration (Personal)"],
        summary="Сhange the configuration of the user's workspace", 
        description=
"""
#### Layout Choices:
- LIST
- BOARD
- CALENDAR
- TABLE
- TIMELINE

#### Order Choices:
- UPDATED_AT
- CREATED_AT
- START_DATE
- DEADLINE
- PRIORITY

#### Group Choices:
- STATE
- PRIORITY
- MODULE
- TAG
- ASSIGNEE
- CREATED_BY
"""
    ),
)


user_workspace_favorite = extend_schema_view(

    get=extend_schema(
        tags=["Workspace: User Favorite"],
        summary="...................................", 
        responses=UserFavoriteReadSerializer
    ),

    patch=extend_schema(
        tags=["Workspace: User Favorite"],
        summary="...................................",
        request=UserFavoriteUpdateSerializer,
        responses=UserFavoriteReadSerializer,
    ),

    post=extend_schema(
        tags=["Workspace: User Favorite"],
        summary="...................................",
        request=UserFavoriteCreateSerializer,
        responses=UserFavoriteReadSerializer,
    ),

    delete=extend_schema(
        tags=["Workspace: User Favorite"],
        summary="...................................",
    ),
)
