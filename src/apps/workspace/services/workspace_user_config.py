from collections.abc import Callable
from dataclasses import dataclass
from django.core.exceptions import ValidationError

from core.services.baseservice import BaseService, GetObjectsByIdService
from apps.workspace.models.workspace import Workspace
from apps.users.models.users import User
from apps.workspace.models.workspace_user_config import (
    DisplayFilters,
    DisplayProperties,
    UserFavorite,
    UserWorkspaceConfig,
)
from typing import Any

from apps.workspace.typing import FavoriteData


@dataclass
class UserWorkspaceConfigCreator(BaseService, GetObjectsByIdService):
    """
    Service for creating a UserWorkspaceConfig
    Also creates and associates these objects with UserWorkspaceConfig: DisplayFilters and DisplayProperties
    """
    user: User | int
    workspace: Workspace | int

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> UserWorkspaceConfig:
        user_wp_config = self.create_user_workspace_config()
        self.create_display_filters(user_wp_config)
        self.create_display_properties(user_wp_config)
        return user_wp_config

    def create_user_workspace_config(self) -> UserWorkspaceConfig:
        return UserWorkspaceConfig.objects.create(
            user=self.user,
            workspace=self.workspace,
        )

    def create_display_filters(
        self, user_wp_config: UserWorkspaceConfig
    ) -> DisplayFilters:
        return DisplayFilters.objects.create(user_workspace_config=user_wp_config)

    def create_display_properties(
        self, user_wp_config: UserWorkspaceConfig
    ) -> DisplayProperties:
        return DisplayProperties.objects.create(user_workspace_config=user_wp_config)


@dataclass
class UserFavoriteCreator(BaseService, GetObjectsByIdService):
    """
    Service for creating a favorite object for the user
    
    """
    user: int | User
    workspace: int | Workspace
    data: FavoriteData

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> UserFavorite:
        self.data["user"] = self.user
        self.data["workspace"] = self.workspace
        return self.create_favorite()

    def create_favorite(self) -> UserFavorite:
        return UserFavorite.objects.create(**self.data)

    def get_validators(self) -> list[Callable[..., Any]]:
        return [
            self.validate_is_folder,
            self.validate_entity_data,
        ]

    def validate_is_folder(self):
        if self.data["is_folder"]:
            # The folder cannot have these parameters
            self.data["entity_type"] = None
            self.data["entity_identifier"] = None
            self.data["parent"] = None

            # Set name
            self.data["name"] = self.data["name"] or "Folder"

    def validate_entity_data(self):
        from core.constants import get_entity_model
        if not self.data["is_folder"]:
            entity_model = get_entity_model(self.data["entity_type"])
            entity_identifier = self.data["entity_identifier"]

            if entity_model and not entity_model.objects.filter(pk=entity_identifier).exists():
                raise ValidationError(f"Object {entity_model} does not exist")

            parent_id = self.data.get("parent")
            if parent_id and not UserFavorite.objects.filter(pk=parent_id).exists():
                raise ValidationError(f"This folder does not exist")
