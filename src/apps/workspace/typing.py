from typing import Optional, TypedDict


class FavoriteData(TypedDict):
    is_folder: bool
    name: str
    entity_type: Optional[str] = None
    entity_identifier: Optional[int] = None
    parent: Optional[int] = None


class WorkspaceData(TypedDict):
    name: str
    description: Optional[str] = None